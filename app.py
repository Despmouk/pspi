# BEGIN CODE HERE
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.common.by import By
from numpy import dot
from numpy.linalg import norm
from selenium.webdriver.chrome.options import Options

# END CODE HERE

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/pspi"
CORS(app)
mongo = PyMongo(app)
mongo.db.products.create_index([("name", TEXT)])


@app.route("/search", methods=["GET"])
def search():
    # BEGIN CODE HERE
    name = request.args.get("name")
    products = mongo.db.products.find({"$text": {"$search": f"\"{name}\""}})
    productsList = list(products)
    productsListSorted = sorted(productsList, key=lambda k: k['price'], reverse=True)
    productsToReturn=[]
    for doc in productsListSorted:
        doc['_id'] = str(doc['_id']) # This does the trick!
        productsToReturn.append(doc)
    return jsonify(productsToReturn), 200
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    new_product = request.json
    exists = mongo.db.products.find_one({"name": new_product["name"]})
    if exists is None:
        mongo.db.products.insert_one(new_product)
        return "Addition made"
    else:
        mongo.db.products.update_many({"name": new_product["name"]}, {"$set": {"price": new_product["price"], "production_year": new_product["production_year"], "color": new_product["color"], "size": new_product["size"]}})
        return "Updated"
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    bodyRequest = request.json
    itemRequest = [bodyRequest["production_year"],bodyRequest["price"],bodyRequest["color"],bodyRequest["size"]]
    products = mongo.db.products.find()
    productsList = list(products)
    similarProducts= []
    for product in productsList:
        itemDB = [product["production_year"],product["price"],product["color"],product["size"]]
        cosSimilarity = dot(itemRequest,itemDB)/(norm(itemRequest)*norm(itemDB))
        if cosSimilarity > 0.7:
            similarProducts.append(product["name"])
    return similarProducts
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    try:
        semester = request.args.get('semester')
        url = "https://qa.auth.gr/el/x/studyguide/600000438/current"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        print(semester)
        element = driver.find_element(By.ID, "exam" + semester)
        elements = element.find_elements(By.TAG_NAME, "a")
        res = []
        for e in elements:
            #takes the text from the paragraph tags
            res.append(e.text) 
        return jsonify(res),200
    except Exception as e:
        return "BAD REQUEST", 400
    
    # END CODE HERE
