function showMenu(restaurantId, event) {
  event.preventDefault();

  fetch(`/get-menu/${restaurantId}`)
      .then(response => {
          if (!response.ok) {
              throw new Error('Failed to fetch menu');
          }
          return response.json(); // Parse the JSON response
      })
      .then(data => {
          const menuContentHTML = data.menu_html; 

          const tempElement = document.createElement('div');
          tempElement.innerHTML = menuContentHTML;
          const extractedMenuContent = tempElement.querySelector('.menu-content').innerHTML;
          
          const menuContent = document.querySelector('.menu-content');
          menuContent.innerHTML = extractedMenuContent;

          
          menuContent.style.display = 'block';
          document.getElementById('mainDetail').style.display = 'none';
      })
      .catch(error => {
          console.error('Error fetching menu:', error);
      });
}


function addToCart(itemId) {
  // Make a POST request to the backend to add the item to the cart
  console.log(itemId);
  var errorDiv = document.getElementById("message");
  fetch(`/add-to-cart/${itemId}`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ item_id: itemId })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Failed to add item to cart');
    } else {
      errorDiv.textContent = "Item added to cart!";
      setTimeout(() => {
        errorDiv.textContent = "";
      }, 1000);
    }
  })
  .catch(error => {
      console.error('Error adding item to cart:', error);
      errorDiv.textContent ="Items from different restaurants exists in cart";
      setTimeout(() => {
        errorDiv.textContent = "";
    }, 2000);
  });
}

