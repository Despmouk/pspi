# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from numpy import dot
from numpy.linalg import norm

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
 data = request.json
    
    if not data:
        return jsonify({"error": "No JSON data provided"}), 400
    
    existing_product = mongo.db.products.find_one({"name": data["name"]})
    if existing_product:
        # Ενημέρωση των πεδίων του υπάρχοντος προϊόντος
        existing_product['price'] = data['price']
        existing_product['production_year'] = data['production_year']
        existing_product['color'] = data['color']
        existing_product['size'] = data['size']
        mongo.db.products.save(existing_product)
        return jsonify({"message": "Product updated successfully"}), 200
    
    # Προσθήκη νέου προϊόντος στη βάση
    mongo.db.products.insert_one(data)
    
    return jsonify({"message": "Product added successfully"}), 201

    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    def calculate_similarity(product1, product2):
        cosine_similarity = dot(product1, product2) / (norm(product1) * norm(product2))
        return cosine_similarity

    given_product = request.get_json()
    given_product_features = [
        given_product.get("production_year"),
        given_product.get("price"),
        given_product.get("color"),
        given_product.get("size"),
    ]
    # TODO: should id and name be included in similarity calculation?
    similar_products = []
    all_products = mongo.db.products.find(
        {},
        {"name": 1, "production_year": 1, "price": 1, "color": 1, "size": 1},
    )
    for product in all_products:
        product_features = [
            product["production_year"],
            product["price"],
            product["color"],
            product["size"],
        ]
        similarity = calculate_similarity(given_product_features, product_features)
        if similarity > 0.7:
            similar_products.append(product["name"])

    return jsonify(similar_products)
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    return ""
    # END CODE HERE
