# BEGIN CODE HERE
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from numpy import dot
from numpy.linalg import norm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    query = request.args.get("name")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    result = list(mongo.db.products.find({"name": query}).sort("price", -1))

    if not result:
        return jsonify({"error": "Product not found"}), 404

    for product in result:
        product["_id"] = str(product["_id"])

    return jsonify(result)

    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    data = request.json

    def check_price(price):
        parts = price.split(".")
        if len(parts) != 2:
            return False
        return parts[0].isnumeric() and parts[1].isnumeric()

    if (
        not data
        or not data["name"].strip()
        or not data.get("production_year").isdigit()
        or not check_price(data.get("price"))
    ):
        return jsonify({"error": "Wrong JSON data provided"}), 400

    # Check valid values for color and size
    valid_colors = ["1", "2", "3"]
    valid_sizes = ["1", "2", "3", "4"]
    if data["color"] not in valid_colors or data["size"] not in valid_sizes:
        return jsonify({"error": "Invalid color or size provided"}), 400

    existing_product = mongo.db.products.find_one({"name": data["name"]})
    if existing_product:
        # Ενημέρωση των πεδίων του υπάρχοντος προϊόντος
        mongo.db.products.update_one(
            {"_id": existing_product["_id"]},
            {"$set": data},
        )
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
            similar_products.append(product)

    return jsonify(similar_products)
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    url = "https:qa.auth.gr/el/x/studyguide/600000438/current"
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    semester = request.args.get("semester")
    driver.get(url)
    print(semester)
    section = driver.find_element(By.ID, "exam" + semester)
    elements = section.find_elements(By.TAG_NAME, "a")
    res = []
    for element in elements:
        res.append(element.text)
    driver.quit()
    return jsonify(res)
    # END CODE HERE


# this is not inside BEGIN and END CODE but how else is the server supposed to run?
if __name__ == "__main__":
    app.run(debug=True)
