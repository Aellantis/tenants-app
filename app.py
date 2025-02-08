from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
# from models.logic import logic_function
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Database setup
client = MongoClient("mongodb://localhost:27017/")
db = client.tenant_app
calculations_collection = db.information


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/home")
def home():
    pass


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/delete/<id>", methods=["POST"])
def delete(_id):
    pass


@app.route("/something/<_id>", methods=["GET"])
def another_func(_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
