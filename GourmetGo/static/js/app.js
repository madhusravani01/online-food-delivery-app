const mainMenusDiv = document.getElementsByClassName("main-menu-child2")[0];

const loginForm = `
        <form id="loginForm" class= "userLogin" onsubmit="required_login(event)">
            <h3>USER LOGIN</h3><br><br>
            <label for="username">Username:</label><br>
            <input type="text" id="user_name" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="user_password" name="password"><br><br>
            <button type="submit" value="Login">Login</button>
        </form>
        <div id="errorMessage"></div>
        <br><br>
        <p>If New User, <a href="#" onclick="openRegistrationForm(event)">Register</a><br><br></p>
        <p>If Admin, <a href="#" onclick="openAdminForm(event)">Click Here</a><br><br></p>
        <p>If Restaurant, <a href="#" onclick="openRestaurantForm(event)">Click Here</a><br><br></p>
        <p>If Delivery Partner, <a href="#" onclick="openDeliveryForm(event)">Click Here</a><br><br></p>
        
    `;


function openUserLoginForm(event) {
    event.preventDefault();
    mainMenusDiv.innerHTML = loginForm;
}

// Function to open registration form
function openRegistrationForm(event) {
    event.preventDefault();
    const registrationForm = `
        <form id="registrationForm" class="registerForm" onsubmit="register_user(event)">
            <h3>REGISTER</h3><br><br>
            <label for="firstname">First Name:</label><br>
            <input type="text" id="first_name" name="firstname"><br>
            <label for="lastname">Last Name:</label><br>
            <input type="text" id="last_name" name="lastname"><br>
            <label for="email">Email:</label><br>
            <input type="text" id="email" name="email"><br>
            <label for="phone_number">Phone Number:</label><br>
            <input type="number" id="phone_number" name="phone_number" min="1000000000" max="9999999999"><br>
            <label for="username">Username:</label><br>
            <input type="text" id="new_username" name="username"><br>
            <label for="password">Password:</label><br>
            <input type="password" id="new_password" name="password"><br>
            <label for="password">Confirm Password:</label><br>
            <input type="password" id="confirm_password" name="password"><br><br>
            <button type="submit" value="Register">Register</button>
        </form>
        <div id="errorMessage"></div>
    `;
    mainMenusDiv.innerHTML = registrationForm;
}

// Function to open admin form
function openAdminForm(event) {
    event.preventDefault();
    const adminForm = `
        <form id="adminForm" class="adminForm" onsubmit="required_admin(event)">
            <h3>ADMIN LOGIN</h3><br><br>
            <label for="username">Username:</label><br>
            <input type="text" id="admin_name" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="admin_password" name="password"><br><br>
            <button type="submit" value="Login">Login</button>
        </form>
        <div id="errorMessage"></div>
    `;
    mainMenusDiv.innerHTML = adminForm;
}

// Function to open restaurant form
function openRestaurantForm(event) {
    event.preventDefault();
    const restaurantForm = `
        <form id="restaurantForm" class="restaurantForm" onsubmit="required_restaurant(event)">
            <h3>RESTAURANT LOGIN</h3><br><br>
            <label for="username">Username:</label><br>
            <input type="text" id="res_name" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="res_password" name="password"><br><br>
            <button type="submit" value="Login">Login</button>
        </form>
        <div id="errorMessage"></div>
    `;
    mainMenusDiv.innerHTML = restaurantForm;
}

// Function to open restaurant form
function openDeliveryForm(event) {
    event.preventDefault();
    const deliveryForm = `
        <form id="deliveryForm" class="deliveryForm" onsubmit="required_delivery(event)">
            <h3>DELIVERY AGENTS LOGIN</h3><br><br>
            <label for="username">Username:</label><br>
            <input type="text" id="del_name" name="username"><br><br>
            <label for="password">Password:</label><br>
            <input type="password" id="del_password" name="password"><br><br>
            <button type="submit" value="Login">Login</button>
        </form>
        <div id="errorMessage"></div>
    `;
    mainMenusDiv.innerHTML = deliveryForm;
}

function required_login(event) {
    event.preventDefault();
    var username = document.getElementById("user_name").value;
    var password = document.getElementById("user_password").value;
    var errorDiv = document.getElementById("errorMessage");

    if (username === "") {
        errorDiv.textContent ="Username cannot be empty.";
        return;
    } else if (password === "") {
        errorDiv.textContent = "Password cannot be empty.";
        return;
    }

    var loginForm = event.target;

    fetch('http://127.0.0.1:5000/validate-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorDiv.textContent = "Username or Password Incorrect. Please try again."; 
        } else {
            window.location.href = '/user_homepage'; 
        }
    })
    .catch(error => console.error('Error:', error));
}


function required_admin(event) {
    event.preventDefault();
    var username = document.getElementById("admin_name").value;
    var password = document.getElementById("admin_password").value;
    var errorDiv = document.getElementById("errorMessage");

    if (username === "") {
        errorDiv.textContent ="Username cannot be empty.";
        return;
    } else if (password === "") {
        errorDiv.textContent = "Password cannot be empty.";
        return;
    }

    var adminForm = event.target;

    fetch('http://127.0.0.1:5000/validate-admin', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorDiv.textContent = "Username or Password Incorrect. Please try again."; 
        } else {
            window.location.href = '/manage_restaurants'; 
        }
    })
    .catch(error => console.error('Error:', error));
}

function required_delivery(event) {
    event.preventDefault();
    var username = document.getElementById("del_name").value;
    var password = document.getElementById("del_password").value;
    var errorDiv = document.getElementById("errorMessage");

    if (username === "") {
        errorDiv.textContent ="Username cannot be empty.";
        return;
    } else if (password === "") {
        errorDiv.textContent = "Password cannot be empty.";
        return;
    }

    var deliveryForm = event.target;

    fetch('http://127.0.0.1:5000/validate-deliveryagent', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorDiv.textContent = "Username or Password Incorrect. Please try again."; 
        } else {
            window.location.href = '/deliveryagent_homepage'; 
        }
    })
    .catch(error => console.error('Error:', error));
}


function required_restaurant(event) {
    event.preventDefault();
    var username = document.getElementById("res_name").value;
    var password = document.getElementById("res_password").value;
    var errorDiv = document.getElementById("errorMessage");

    if (username === "") {
        errorDiv.textContent ="Username cannot be empty.";
        return;
    } else if (password === "") {
        errorDiv.textContent = "Password cannot be empty.";
        return;
    }

    var restaurantForm = event.target;

    fetch('/validate-restaurant', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorDiv.textContent ="Invalid credentials. Please try again."
        } else if (data.reset_password) {
            window.location.href = '/reset_password';  // Redirect to reset password page
        } else if (data.success) {
            window.location.href = '/restaurant_homepage';  // Redirect to homepage
        }
    })
    .catch(error => console.error('Error:', error));
}

function register_user(event) {
    event.preventDefault();
    var firstname = document.getElementById("first_name").value;
    var lastname = document.getElementById("last_name").value;
    var email = document.getElementById("email").value;
    var phone_number = document.getElementById("phone_number").value;
    var username = document.getElementById("new_username").value;
    var password = document.getElementById("new_password").value;
    var confirmPassword = document.getElementById("confirm_password").value;
    var errorDiv = document.getElementById("errorMessage");

    if(firstname === ""){
        errorDiv.textContent ="First Name cannot be empty.";
        return;
    }else if(lastname === ""){
        errorDiv.textContent ="Last Name cannot be empty.";
        return;
    }else if(email === ""){
        errorDiv.textContent ="Email Address cannot be empty.";
        return;
    }else if(phone_number === ""){
        errorDiv.textContent ="Phone Number cannot be empty.";
        return;
    }else if(username === ""){
        errorDiv.textContent ="Username cannot be empty.";
        return;
    }else if(password === ""){
        errorDiv.textContent ="Password cannot be empty.";
        return;
    }else if(confirmPassword === "" || password !== confirmPassword){
        errorDiv.textContent ="Please confirm your password. Both password fields should match.";
        return;
    }

    var registerForm = event.target;

    fetch('http://127.0.0.1:5000/register-user', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `firstname=${firstname}&lastname=${lastname}&email=${email}&phone_number=${phone_number}&username=${username}&password=${password}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            errorDiv.textContent = "User already exists"; 
        } else {
            errorDiv.textContent = "User registered successfully.Redirecting to User login."; 
            setTimeout(() => {
                mainMenusDiv.innerHTML = loginForm;
            }, 5000); 
        }
    })
    .catch(error => console.error('Error:', error));
}

