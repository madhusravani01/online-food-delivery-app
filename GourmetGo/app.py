from datetime import datetime
from flask import Flask, abort ,flash, jsonify,session,render_template,redirect,url_for,request
import os
import cgitb; cgitb.enable()
from werkzeug.utils import secure_filename
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask import request, session, redirect, url_for
from datetime import datetime
import json


app = Flask(__name__)
app.secret_key = 'secret key'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config["MONGO_DBNAME"] = "GourmetGo"
app.config["MONGO_URI"] = "mongodb://localhost:27017/GourmetGo"
mongo = PyMongo(app)

current_time = datetime.now()

#homepage
@app.route('/')
def homepage():
	if session:
		session.pop('username', None)					#used to logout of current session
	return render_template('homepage.html')

#customer session is created after log in
@app.route('/validate-user', methods=['GET', 'POST'])
def validate_user():
    username = request.form.get('username')
    password = request.form.get('password')

    user = mongo.db.customer.find_one({"username": username})

    if not user:
        return jsonify({'error': 'User not found'})
     
    if password == user['password']:
        session['username'] = username
        return jsonify({'success': True}) 
    else:
        flash('Incorrect password')
        return jsonify({'error': 'Incorrect password'})
    
#customer session is created after log in
@app.route('/validate-admin', methods=['GET', 'POST'])
def validate_admin():
    admin_uname = request.form.get('username')
    admin_pwd = request.form.get('password')

    admin = mongo.db.admin.find_one({"user_name": admin_uname})

    if not admin:
        return jsonify({'error': 'User not found'})
     
    if admin_pwd == admin['password']:
        session['admin_name'] = admin_uname
        return jsonify({'success': True}) 
    else:
        flash('Incorrect password')
        return jsonify({'error': 'Incorrect password'})
    
@app.route('/validate-restaurant', methods=['POST'])  
def validate_restaurant():
    res_uname = request.form.get('username')
    res_pwd = request.form.get('password')

    restaurant = mongo.db.restaurant.find_one({"email_address": res_uname})

    if not restaurant:
        return jsonify({'error': 'User not found'})
    
    if res_pwd == restaurant['password']:
        session['restaurant_name'] = res_uname
        if restaurant['login_count'] == 0:
            return jsonify({'reset_password': True})  
        else: 
            return jsonify({'success': True})  
    else:
        return jsonify({'error': 'Incorrect password'}) 
    
    
@app.route('/validate-deliveryagent', methods=['GET', 'POST'])
def validate_deliveryagent():
    del_uname = request.form.get('username')
    del_pwd = request.form.get('password')

    delivery_agent = mongo.db.delivery_agents.find_one({"email_address": del_uname})

    if not delivery_agent:
        return jsonify({'error': 'User not found'})
     
    if del_pwd == delivery_agent['password']:
        session['delivery_agent'] = del_uname
        return jsonify({'success': True}) 
    else:
        flash('Incorrect password')
        return jsonify({'error': 'Incorrect password'})


@app.route('/register-user', methods=['GET', 'POST'])
def register_user():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    username = request.form.get('username')
    password = request.form.get('password')

    user = mongo.db.customer.find_one({"email_address": email}) 
    if user:
        return jsonify({'error': 'User already exists'})
    else:
        session['username'] = request.form['username']
        password = request.form['password']

        new_customer = {
            "first_name" : firstname,
            "last_name" : lastname,
            "email_address": email,
            "phone_number" : phone_number,
            "username" : username,
            "password": password,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        mongo.db.customer.insert_one(new_customer)
        return jsonify({'success': True}) 


#when customer wants to logout
@app.route('/logout')
def customer_logout():
	session.pop('username', None)		
	return redirect(url_for('homepage'))

@app.route('/reset_password')
def reset_password():
    return render_template('reset_password.html')

@app.route('/add_menu_category')
def add_menu_category():
    return render_template('add_menu_category.html')

@app.route('/update_password', methods=['POST'])
def update_password():
    input_password = request.form.get('inputPassword')
    new_password = request.form.get('newPassword')
    res_uname = session.get('restaurant_name')
    restaurant = mongo.db.restaurant.find_one({"email_address": res_uname})

    if restaurant:
        old_password = restaurant['password']
        if(old_password == input_password):
            mongo.db.restaurant.update_one(
                {"email_address": res_uname},
                {"$set": {"password": new_password, "login_count": 1}}
            )
            return jsonify({"success": True, "message": "Password updated successfully."}), 200
        else: 
            return jsonify({"error": "Old Password is wrong. Please try again."}), 404
    else:
        return jsonify({"error": "User not found."}), 404

#homepage of customer where restaurants are needed to be selected
@app.route('/user_homepage')
def user_homepage():
    restaurants = list(mongo.db.restaurant.find())
    return render_template('user_homepage.html', restaurants = restaurants)

@app.route('/render_delete_restaurant', methods=['GET','POST'])
def render_delete_restaurant():
    return render_template('delete_restaurant.html')

@app.route('/render_add_restaurant', methods=['GET','POST'])
def render_add_restaurant():
    return render_template('add_restaurant.html')

@app.route('/render_delete_menu', methods=['GET','POST'])
def render_delete_menu():
    return render_template('delete_menu.html')

@app.route('/render_add_menu')
def render_add_menu():
    restaurant_id = request.args.get("restaurant_id")
    categories = list(mongo.db.menu_category.find({"restaurant_id": ObjectId(restaurant_id)}, {"category_name": 1, "_id": 0}))
    category_names = [category['category_name'] for category in categories]
    return render_template('add_menu.html', restaurant_id=restaurant_id, category_names=category_names)

@app.route('/render_add_deliveryagent', methods=['GET','POST'])
def render_add_deliveryagent():
    return render_template('add_deliveryagent.html')

@app.route('/render_delete_deliveryagent', methods=['GET','POST'])
def render_delete_deliveryagent():
    return render_template('delete_deliveryagent.html')


@app.route('/restaurant_homepage')
def restaurant_homepage():
    restaurant_name = session['restaurant_name']
    
    restaurant = mongo.db.restaurant.find_one({'email_address': restaurant_name})
    
    if restaurant:
        restaurant_id = restaurant['_id']
    else:
        return None
    
    restaurant_orders = mongo.db.orders.find({
    "$and": [
        {"restaurant_id": restaurant_id},
        {"status": "pending"}
    ]
    })
    
    return render_template('restaurant_homepage.html', restaurant_orders = restaurant_orders)

@app.route('/accepted_orders')
def accepted_orders():
    restaurant_name = session['restaurant_name']
    
    restaurant = mongo.db.restaurant.find_one({'email_address': restaurant_name})
    delivery_agents = mongo.db.delivery_agents.find({'status': 'available'})
    
    if restaurant:
        restaurant_id = restaurant['_id']
    else:
        return None
    
    delivery_agent_names = [agent['delivery_agent_name'] for agent in delivery_agents]

    restaurant_orders = mongo.db.orders.find({
    "$and": [
        {"restaurant_id": restaurant_id},
        {"status": "preparing"}
    ]
    })
    
    return render_template('restaurant_orders.html', restaurant_orders = restaurant_orders,
                           delivery_agent_names=delivery_agent_names)

@app.route('/deliveryagent_orders')
def deliveryagent_orders():
    delivery_agent_email = session['delivery_agent'] 
    
    delivery_agent = mongo.db.delivery_agents.find_one({"email_address" : delivery_agent_email})
    
    delivery_agent_name = delivery_agent['delivery_agent_name']
    
    assigned_orders = mongo.db.orders.find({"delivery_agent_name": delivery_agent_name,
                                            "status": "on the way"})


    orders_data = []
    for order in assigned_orders:
        # Get the restaurant details associated with each order
        restaurant = mongo.db.restaurant.find_one({"_id": order['restaurant_id']})

        order_details = {
            'order_id': order['_id'],
            'status': order['status'],
            'restaurant_name': restaurant['restaurant_name'],
            'location' : restaurant['location']
            # Add other relevant order and restaurant details
        }
        orders_data.append(order_details)
    return render_template('deliveryagent_orders.html', order_data= orders_data)


@app.route('/update-order/<order_id>', methods=['PUT'])
def update_order(order_id):
    data = request.get_json()

    if not data or 'status' not in data:
        return jsonify({'error': 'Invalid request'}), 400
    
    new_status = data['status']

    # Example pseudocode:
    order = mongo.db.orders.find_one({'_id': ObjectId(order_id)})
    if order:
        mongo.db.orders.update_one(
            {'_id': ObjectId(order_id)},
            {'$set': {'status': new_status}}
        )
        
        if new_status == 'on the way':
            count = mongo.db.delivery_agents.count_documents(
                {'delivery_agent_name': order['delivery_agent_name'], 'status': 'busy'},
            )
            if count == 0: 
                mongo.db.delivery_agents.update_one(
                    {'delivery_agent_name': order['delivery_agent_name'], 'status': 'available'},
                    {'$set': {'status': 'busy'}}
                )
            else:
                return jsonify({'error': 'You already have an order to deliver.'})
               
        if new_status == 'delivered':
            mongo.db.delivery_agents.update_one(
                {'delivery_agent_name': order['delivery_agent_name'], 'status': 'busy'},
                {'$set': {'status': 'available'}}
            )
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Order not found'}), 404
    
@app.route('/deliveryagent_homepage')
def deliveryagent_homepage():
    delivery_agent_email = session['delivery_agent'] 
    
    delivery_agent = mongo.db.delivery_agents.find_one({"email_address" : delivery_agent_email})
    
    delivery_agent_name = delivery_agent['delivery_agent_name']
    
    assigned_orders = mongo.db.orders.find({"delivery_agent_name": delivery_agent_name, 
                                            "status": "delivery agent assigned"})


    orders_data = []
    for order in assigned_orders:
        # Get the restaurant details associated with each order
        restaurant = mongo.db.restaurant.find_one({"_id": order['restaurant_id']})

        order_details = {
            'order_id': order['_id'],
            'status': order['status'],
            'restaurant_name': restaurant['restaurant_name'],
            'location' : restaurant['location']
            # Add other relevant order and restaurant details
        }
        orders_data.append(order_details)
    return render_template('deliveryagent_homepage.html', order_data= orders_data)

@app.route('/get-menu/<restaurantId>')
def get_menu(restaurantId):
    menu_list = mongo.db.menu.find({"restaurant_id": restaurantId})
    # Convert ObjectId to string for each document
    menu_list = [
        {**menu, '_id': str(menu['_id'])}  # Convert ObjectId to string
        for menu in menu_list
    ]

    # Render an HTML template as a string
    menu_html = render_template('user_homepage.html', menu_lists=menu_list)

    # Return the HTML content as a response
    return jsonify(menu_html=menu_html)

from flask import render_template

@app.route('/cart')
def show_cart():
    username = session['username']
    customer = mongo.db.customer.find_one({'username': username})
    if customer:
        customer_id = customer['_id']
    else:
        return None

    query = {
        "customer_id": ObjectId(customer_id),
        "status": "cart"
    }

    order = mongo.db.orders.find_one(query)
    
    if order:
        subtotal = 0
        total = 0
        items_in_cart = []

        items = order.get("items", [])
        for item in items:
            item_id = item.get("item_id")
            item_name= item.get("item_name")
            restaurant_id = item.get("restaurant_id")
            quantity = item.get("quantity", 0)
            fetched_item = get_item(item_id)
            if fetched_item:
                item_price = float(fetched_item.get("item_price"))
                subtotal += item_price * quantity
                final_subtotal="{:.2f}".format(subtotal)

                items_in_cart.append({
                    "item_id" :item_id,
                    "item_name": item_name,
                    "quantity": quantity,
                    "item_price": item_price,
                    "subtotal": final_subtotal
                })

        total = subtotal * 1.08  # Calculate total including tax
        session['order_info'] = {
            'order_id': str(order['_id']),
            'customer_id': str(customer_id),
            'subtotal': final_subtotal,
            'total': total
        }
    
        return render_template(
            "view_cart.html",
            order = order,
            items_in_cart=items_in_cart,
            total="{:.2f}".format(total),
            subtotal=final_subtotal,
            tax="{:.2f}".format(subtotal * 0.08)
        )
    else:
        return render_template("no_orders.html")
        
@app.route('/add-to-cart/<item_id>', methods=['POST'])
def add_to_cart(item_id):
    username = session['username']
    customer = mongo.db.customer.find_one({'username': username})

    if customer:
        customer_id = customer['_id']
    else:
        return None
    
    item = get_item(item_id)
    restaurant_id = item.get('restaurant_id') 
    item_name = item.get('item_name')
    
    existing_order = mongo.db.orders.find_one({
    "customer_id": customer_id,
    "status": "cart"
    })

    if existing_order:
    # Check if the item exists in the items array
        item_exists = False
        for existing_item in existing_order["items"]:
            existing_restaurant_id = get_item(existing_item["item_id"]).get("restaurant_id")
            if existing_restaurant_id != restaurant_id:
                abort(400, description='Some error message')
            if existing_item["item_id"] == ObjectId(item_id):
            # If the item exists, increment the quantity
                mongo.db.orders.update_one({
                    "_id": ObjectId(existing_order["_id"]),
                    "items.item_id":  ObjectId(item_id)
                }, {
                    "$inc": {"items.$.quantity": 1}
                })
                item_exists = True
                break
    
        # If the item doesn't exist, add a new item to the items array
        if not item_exists:
            mongo.db.orders.update_one({
                "_id": existing_order["_id"]
            }, {
                "$push": {
                    "items": {
                        "item_id":  ObjectId(item_id),
                        "item_name": item_name,
                        "quantity": 1
                    }
                }
            })
    else:
    # If the order doesn't exist, create a new one with the item
        new_order = {
            "customer_id": customer_id,
            "restaurant_id" : ObjectId(restaurant_id),
            "status": "cart",
            "date": current_time,
            "items": [
                {
                    "item_id": ObjectId(item_id),
                    "item_name": item_name,
                    "quantity": 1
                }
            ]
        }
        mongo.db.orders.insert_one(new_order)
    return jsonify({'success': True})
    
    
@app.route('/update-cart/<item_id>', methods=['POST'])
def update_cart(item_id):
    # Retrieve the item ID and new quantity from the request
    new_quantity = int(request.json.get('quantity'))
    
    username = session['username']
    customer = mongo.db.customer.find_one({'username': username})

    if customer:
        customer_id = customer['_id']
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404

    existing_order = mongo.db.orders.find_one({
        "customer_id": customer_id,
        "status": "cart"
    })

    if existing_order:
        # Update the quantity for the specified item ID
        mongo.db.orders.update_one({
            "_id": ObjectId(existing_order["_id"]),
            "items.item_id": ObjectId(item_id)
        }, {
            "$set": {"items.$.quantity": new_quantity}
        })
        return jsonify({'success': True, 'message': 'Quantity updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'Cart not found'}), 404

@app.route('/remove/<item_id>/<order_id>', methods=['GET','POST'])
def remove(item_id,order_id):

    # Remove the specific item from the items array within the order
    query = {
        "_id": ObjectId(order_id),
        "status": "cart",
        "items.item_id": ObjectId(item_id),
    }
    update_operation = {"$pull": {"items": {"item_id": ObjectId(item_id)}}}
    mongo.db.orders.update_one(query, update_operation)

    # Check if the order now has an empty items array
    empty_items_order = mongo.db.orders.find_one({"_id": ObjectId(order_id),
                                                  "items": {"$exists": True, "$eq": []}})

    # If the order's items array is empty, delete the order
    if empty_items_order:
        mongo.db.orders.delete_one({"_id": ObjectId(order_id)})
        return redirect("/cart")

    return redirect("/cart")


@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template("payment.html")

@app.route('/place_order', methods=['GET','POST'])
def place_order():
    payment_method = request.args.get('payment')
    order_info = session.get('order_info')

    if order_info:
        order_id = order_info.get('order_id')
        customer_id = order_info.get('customer_id')
        subtotal = order_info.get('subtotal')
        total = order_info.get('total')

    order = mongo.db.orders.find_one({"_id":ObjectId( order_id )})
    
    if order:
        # Update the order status to "pending"
        mongo.db.orders.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": {"status": "pending"}}
        )

    payment_data = {
        "order_id": order_id,
        "customer_id": ObjectId(customer_id),
        "amount": total,
        "subtotal": subtotal,
        "payment_method": payment_method,
        "payment_status": "Paid" if payment_method == "cash" else "Pending",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    # Insert the payment into the database
    mongo.db.payments.insert_one(payment_data)
    return redirect('/orders')

    
@app.route('/card_payment', methods=['GET', 'POST'])
def card_payment():
    return render_template("card_payment.html")

@app.route('/update-delivery-info/<orderId>', methods=['PUT'])
def update_delivery_info(orderId):
    data = request.get_json()
    if not data or 'status' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    new_status = data['status']
    
    order = mongo.db.orders.find_one({'_id': ObjectId(orderId)})
    if order:
        existing_status = order['status']
        if new_status == 'delivered' and existing_status != 'on the way':
            return jsonify({'error': 'The order is not accepted yet'}), 400

        update_query = {}
        if new_status == 'prepared':
            update_query['$set'] = {'status': new_status}
            update_query['$unset'] = {'delivery_agent_name': ''}
        else:
            update_query['$set'] = {'status': new_status}

        mongo.db.orders.update_one(
            {'_id': ObjectId(orderId)},
            update_query
        )
        return jsonify({'success': True}), 200
    else:
        return jsonify({'error': 'Order not found'}), 404

@app.route('/orders')
def show_orders():
    username = session.get('username')
    if not username:
        return "Username not found in session"

    customer = mongo.db.customer.find_one({'username': username})
    if not customer:
        return "Customer not found"

    customer_id = customer['_id']
    orders = mongo.db.orders.find({"customer_id": ObjectId(customer_id)})

    order_details = []
    for order in orders:
        order_id = str(order['_id'])
        order_status = order['status']
        payment = mongo.db.payments.find_one({"order_id": order_id})
       
        if payment:
            updated_date = payment.get('updated_at', None)
            amount = payment.get('amount', None)

            items_details = []
            for item in order['items']:
                item_name = item['item_name']
                quantity = item['quantity']
                items_details.append({
                    'item_name': item_name,
                    'quantity': quantity
                })

            order_details.append({
                'order_id': order_id,
                'updated_date': updated_date.strftime("%Y-%m-%d") if updated_date else None,
                'items': items_details,
                'order_status': order_status,
                'amount': "{:.2f}".format(amount)
            })

    return render_template('orders.html', order_details=order_details)

@app.route('/assign_da')
def assign_da():
    prepared_orders = mongo.db.orders.find({"status": "prepared"})
    
    prepared_orders_details = []
    for order in prepared_orders:
        restaurant = mongo.db.restaurant.find_one({"_id": order['restaurant_id']})
        order_details = {
            'order_id': order['_id'],
            'status': order['status'],
            'restaurant_name': restaurant['restaurant_name'],
            'restaurant_email': restaurant['email_address'],
        }
        prepared_orders_details.append(order_details)

    delivery_agents = mongo.db.delivery_agents.find({'status': 'available'})
    delivery_agent_names = [agent['delivery_agent_name'] for agent in delivery_agents]

    return render_template('assign_da.html', 
                           prepared_orders_details=prepared_orders_details,
                           delivery_agent_names=delivery_agent_names)

@app.route('/assign_delivery_agent/<order_id>', methods=['PUT'])
def assign_delivery_agents(order_id):
    data = request.get_json()
    if not data or 'delivery_agent_name' not in data:
        return jsonify({'error': 'Invalid request, missing delivery agent name'}), 400

    delivery_agent_name = data['delivery_agent_name']

    mongo.db.orders.update_one(
        {'_id': ObjectId(order_id)},
        {'$set': {
            'delivery_agent_name': delivery_agent_name,
            'status': 'delivery agent assigned'
        }}
    )
    
    return jsonify({'success': 'Delivery agent assigned successfully'})

@app.route('/manage_delivery_agents')
def manage_delivery_agents():
    delivery_agents = list(mongo.db.delivery_agents.find())

    return render_template('manage_delivery_agents.html', delivery_agents=delivery_agents)

@app.route('/manage_restaurants')
def manage_restaurants():
    restaurants = list(mongo.db.restaurant.find())

    return render_template('manage_restaurant.html', restaurants=restaurants)

@app.route('/manage_menu')
def manage_menu():
    restaurant_name = session['restaurant_name']
    restaurant = mongo.db.restaurant.find_one({'email_address': restaurant_name})

    if restaurant:
        restaurant_id = restaurant.get('_id')  # Retrieve _id from restaurant
        if restaurant_id:
        # Check the type and convert if necessary
            if not isinstance(restaurant_id, str):
                restaurant_id = str(restaurant_id)
                
                menus = list(mongo.db.menu.find({"restaurant_id": restaurant_id}))
                return render_template('manage_menu.html', restaurant=restaurant, menus=menus)
            else:
                return "No restaurant ID found."
        else:
            return "Restaurant not found."
    
@app.route('/delete_restaurant')
def delete_restaurant():
    restaurant_id = request.args.get("restaurant_id")
    
    result = mongo.db.restaurant.delete_one({"_id": ObjectId(restaurant_id)})
        
    if result:
        return redirect("/manage_restaurants")
    
    
@app.route('/delete_deliveryagent')
def delete_deliveryagent():
    delivery_agent_id = request.args.get("delivery_agent_id")
    
    result = mongo.db.delivery_agents.delete_one({"_id": ObjectId(delivery_agent_id)})
        
    if result:
        return redirect("/manage_delivery_agents")
    
@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    restaurantName = request.form.get('restaurantName')
    email = request.form.get('email')
    password = request.form.get('password')
    location = request.form.get('location')
    contact = request.form.get('contact')
    image = request.files['image']  

    query = {"restaurantName": restaurantName}
    count = mongo.db.restaurant.count_documents(query)
    if count == 0:
        if image:
            path = os.path.join(APP_ROOT, 'static/images', image.filename)
            image.save(path)
        else:
            filename = '' 
        
        restaurant = {
            'restaurant_name': restaurantName,
            'email_address': email,
            'password': password,
            'phone_number': contact,
            'location': location,
            'image': image.filename,
            'login_count' : 0
        }

        mongo.db.restaurant.insert_one(restaurant)
        
        return redirect('/manage_restaurants')  
    else:
        return jsonify({'error': 'Restaurant already exists!'}), 400

@app.route('/add_menu', methods=['POST'])
def add_menu():
    restaurant_id = request.form.get('restaurantId')
    itemName = request.form.get('itemName')
    itemPrice = request.form.get('itemPrice')
    itemCategory = request.form.get('itemCategory')
    itemIngredients = request.form.get('itemIngredients')
    ingredients_list = [ingredient.strip() for ingredient in itemIngredients.split(',')]
    itemImage = request.files['itemImage']

    query = {"item_name": itemName, "restaurant_id": restaurant_id}
    count = mongo.db.menu.count_documents(query)
        
    if count == 0:
        if itemImage:
            path = os.path.join(APP_ROOT, 'static/images', itemImage.filename)
            itemImage.save(path)
        else:
            filename = ''
            
        menu_item = {
            'restaurant_id': restaurant_id,
            'item_name': itemName,
            'item_price': itemPrice,
            'item_category' : itemCategory,
            'item_ingredient': ingredients_list,
            'item_image': itemImage.filename
        }

        mongo.db.menu.insert_one(menu_item)
            
        return redirect('/manage_menu')
    else:
        return jsonify({'error': 'Menu item already exists for this restaurant!'}), 400
    
@app.route('/add_deliveryagent', methods=['POST'])
def add_deliveryagent():
    agentName = request.form.get('agentName')
    agentEmail = request.form.get('agentEmail')
    agentPassword = request.form.get('agentPassword')
    agentContact = request.form.get('agentContact')

    query = {"delivery_agent_name": agentName,"email_address" : agentEmail }
    count = mongo.db.delivery_agents.count_documents(query)
    if count == 0:
        delivery_agent = {
            'delivery_agent_name': agentName,
            'email_address': agentEmail,
            'password': agentPassword,
            'phone_number': agentContact,
            'status': "available"
        }

        mongo.db.delivery_agents.insert_one(delivery_agent)
        
        return redirect('/manage_delivery_agents') 
    else:
        return jsonify({'error': 'Delivery Agent already exists!'}), 400

    
@app.route('/delete_menu')
def delete_menu():
    item_id = request.args.get("item_id")
    
    item = get_item(item_id)
    restaurant_id= item['restaurant_id']
    
    result = mongo.db.menu.delete_one({"_id": ObjectId(item_id)})
    if result:
        return redirect('/manage_menu')
    
@app.route('/menu_category', methods=['GET', 'POST'])
def menu_category():
    if request.method == 'GET':
        # Fetch all menu categories for a restaurant
        res_uname = session.get('restaurant_name')
        restaurant = mongo.db.restaurant.find_one({"email_address": res_uname})
        if restaurant:
            restaurant_id = str(restaurant['_id'])

            menu_categories = list(mongo.db.menu_category.find({"restaurant_id": ObjectId(restaurant_id)}, {"_id": 0}))

            # Convert ObjectId to string representation
            for category in menu_categories:
                category['restaurant_id'] = str(category['restaurant_id'])

            return jsonify(menu_categories)
        else:
            return jsonify({"error": "Restaurant not found"})

    elif request.method == 'POST':
        res_uname = session.get('restaurant_name')
        restaurant = mongo.db.restaurant.find_one({"email_address": res_uname})
        if restaurant:
            restaurant_id = str(restaurant['_id'])

            menu_category_name = request.form.get('menu_category')  # Get menu category from the form

            existing_category = mongo.db.menu_category.find_one({
                "restaurant_id": ObjectId(restaurant_id),
                "category_name": menu_category_name
            })

            if existing_category:
                print("Here.............")
                return jsonify({"error": "Category already exists"})
            else:
                # Create a new menu category
                mongo.db.menu_category.insert_one({
                    "restaurant_id": ObjectId(restaurant_id),
                    "category_name": menu_category_name
                })
                return jsonify({"success": "Category added successfully"})
        else:
            return jsonify({"error": "Restaurant not found"})
    else:
        return jsonify({"error": "Invalid request"})


def get_item(itemId):
    query = {"_id": ObjectId(itemId)}
    item = mongo.db.menu.find_one(query)
    return item


if __name__ == '__main__':
   app.run(debug = True)	
   