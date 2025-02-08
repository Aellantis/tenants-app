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

# Collections
tenants_collection = db.tenants
payments_collection = db.payments
transactions_collection = db.transactions

# Example Schema:

#     Database: tenant_app

#         Collection 1: tenants (stores renter information)

# {
#   "_id": ObjectId("tenant123"),
#   "name": "John Doe",
#   "email": "john@example.com",
#   "phone": "123-456-7890",
#   "unit_number": "A102",
#   "lease_start": "2024-01-01",
#   "lease_end": "2025-01-01"
# }

# Collection 2: payments (stores payment records)

# {
#   "_id": ObjectId("payment567"),
#   "tenant_id": ObjectId("tenant123"),
#   "amount": 1200.00,
#   "payment_method": "credit_card",
#   "payment_date": "2024-02-01",
#   "status": "completed"
# }

# Collection 3: transactions

# {
# "_id": ObjectId("txn789"),
# "tenant_id": ObjectId("tenant123"),
# "payment_id": ObjectId("payment567"),
# "amount": 1200.00,
# "payment_method": "credit_card",
# "transaction_status": "completed",
#  Possible values:

# "pending"
# "completed"
# "failed"
# "transaction_date": "2024-02-01T14:30:00Z",
# "gateway_response": {
#     "transaction_id": "tx_987654321",
#     "status": "approved",
#     "gateway": "Stripe"
#   }
# }


@app.route("/")
def index():
    return render_template("home.html")


@app.route("/payment")
def payment():
    return render_template("payment.html")


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
