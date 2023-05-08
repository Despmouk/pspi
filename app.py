# BEGIN CODE HERE
from ssl import Options
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from pymongo import TEXT
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    list_of_products=[]
    name = request.args.get("name")
    productsArray = mongo.db.products.find({"$text": {"$search": f"\"{name}\""}}).toArray()
    productsArray = sorted(productsArray, key=lambda k: k['price'], reverse=True)
    for x in productsArray:
        list_of_products.append(x)
    return jsonify(list_of_products)
    #https://www.digitalocean.com/community/tutorials/python-check-if-string-contains-another-string
    # END CODE HERE


@app.route("/add-product", methods=["POST"])
def add_product():
    # BEGIN CODE HERE
    new_product = request.json
    exists = mongo.db.products.findOne({"name": new_product["name"]})
    if exists is not None:
        mongo.db.products.update_many({"name": new_product["name"]}, {"$set": {"price": new_product["price"], "production_year": new_product["production_year"], "color": new_product["color"], "size": new_product["size"]}})
    else:
        mongo.db.products.insert_one(new_product)
    return "Addition made"
    # END CODE HERE


@app.route("/content-based-filtering", methods=["POST"])
def content_based_filtering():
    # BEGIN CODE HERE
    bodyRequest = request.json
    products = mongo.db.products.find().toArray() #na einai list
    similarProducts= []
    for product in products:
        cosSimilarity = dot(bodyRequest,product)/(norm(bodyRequest)*norm(product))
        if cosSimilarity > 70: # na einai > 70%
            similarProducts.append(product)
    return jsonify(similarProducts)
    # END CODE HERE


@app.route("/crawler", methods=["GET"])
def crawler():
    # BEGIN CODE HERE
    try:
        semester = request.json
        url = "https://qa.auth.gr/el/x/studyguide/600000438/current"
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        if semester==1:
            elements = driver.find_elements(By.ID, "exam1")
        elif semester==2:
            elements = driver.find_elements(By.ID, "exam2")
        elif semester==3:
            elements = driver.find_elements(By.ID, "exam3")
        elif semester==4:
            elements = driver.find_elements(By.ID, "exam4")
        elif semester==5:
            elements = driver.find_elements(By.ID, "exam5")
        elif semester==6:
            elements = driver.find_elements(By.ID, "exam6")
        elif semester==7:
            elements = driver.find_elements(By.ID, "exam7")
        elif semester==8:
            elements = driver.find_elements(By.ID, "exam8")
        element = elements.find_elements(By.TAG_NAME, "a")    
        res = []
        for e in element:
            res.append(e.text)
        return jsonify(res),200
    except Exception as e:
        return "BAD REQUEST", 400
    
    # END CODE HERE
