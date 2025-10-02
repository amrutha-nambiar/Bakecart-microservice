const productList = document.getElementById('product-list');
const orderList = document.getElementById('order-list');
const orderForm = document.getElementById('order-form');

const PRODUCT_URL = "http://localhost:5001/products";
const ORDER_URL = "http://localhost:5002/orders";

// Fetch products
async function loadProducts() {
    const res = await fetch(PRODUCT_URL);
    const products = await res.json();
    productList.innerHTML = '';
    products.forEach(p => {
        const li = document.createElement('li');
        li.textContent = `ID: ${p.id}, Name: ${p.name}, Price: $${p.price}`;
        productList.appendChild(li);
    });
}

// Fetch orders
async function loadOrders() {
    const res = await fetch(ORDER_URL);
    const orders = await res.json();
    orderList.innerHTML = '';
    orders.forEach(o => {
        const li = document.createElement('li');
        let productInfo = o.product ? JSON.stringify(o.product) : "No product info";
        li.textContent = `Order ID: ${o.order_id}, Product ID: ${o.product_id}, Quantity: ${o.quantity}, Product: ${productInfo}`;
        orderList.appendChild(li);
    });
}

// Handle form submission
orderForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const product_id = parseInt(document.getElementById('product_id').value);
    const quantity = parseInt(document.getElementById('quantity').value);

    await fetch(ORDER_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({product_id, quantity})
    });

    loadOrders();
});

loadProducts();
loadOrders();
