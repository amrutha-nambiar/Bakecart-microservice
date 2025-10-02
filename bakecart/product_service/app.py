from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory product storage
products = [
    {"id": 1, "name": "Chocolate Cake", "price": 20},
    {"id": 2, "name": "Blueberry Muffin", "price": 5},
    {"id": 3, "name": "Croissant", "price": 3}
]

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["POST"])
def add_product():
    data = request.json
    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Invalid product data"}), 400
    new_id = max(p["id"] for p in products) + 1 if products else 1
    new_product = {"id": new_id, "name": data["name"], "price": data["price"]}
    products.append(new_product)
    return jsonify(new_product), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
