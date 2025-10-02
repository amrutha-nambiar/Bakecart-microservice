from flask import Flask, jsonify, request
import requests
import os

app = Flask(__name__)

orders = {}  # in-memory order storage

PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:5001")

@app.route("/orders", methods=["GET"])
def get_all_orders():
    return jsonify(list(orders.values()))

@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    # Fetch product details
    try:
        resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{order['product_id']}", timeout=3)
        resp.raise_for_status()
        order_copy = order.copy()
        order_copy["product"] = resp.json()
    except requests.exceptions.RequestException:
        order_copy = order.copy()
        order_copy["product"] = {"error": "Product service unavailable"}

    return jsonify(order_copy)

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    if not data or "product_id" not in data or "quantity" not in data:
        return jsonify({"error": "Invalid order data"}), 400

    new_id = max(orders.keys()) + 1 if orders else 1
    orders[new_id] = {
        "order_id": new_id,
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    }
    return jsonify(orders[new_id]), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
