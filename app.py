from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
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
app.config["MONGO_URI"] = "mongodb://localhost:27017/tenant_app"
mongo = PyMongo(app)

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
#  (Possible values:

# "pending"
# "completed"
# "failed")
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


@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        # Assuming tenant_id is stored in session
        tenant_id = request.form.get("tenant_id")
        amount = float(request.form.get("amount"))
        payment_method = request.form.get("payment_method")
        payment_date = request.form.get("payment_date")
        transaction_status = "pending"

        if not tenant_id or not amount or not payment_method or not payment_date:
            flash("All fields are required.", "danger")
            return redirect(url_for("payment"))

        try:
            tenant_id = ObjectId(tenant_id)
            amount = float(amount)
        except ValueError:
            flash("Invalid data format.", "danger")
            return redirect(url_for("payment"))

        payment_record = {
            "tenant_id": ObjectId(tenant_id),
            "amount": amount,
            "payment_method": payment_method,
            "payment_date": payment_date,
            "status": "completed"
        }
        payment_id = payments_collection.insert_one(payment_record).inserted_id

        transaction_record = {
            "tenant_id": ObjectId(tenant_id),
            "payment_id": payment_id,
            "amount": amount,
            "payment_method": payment_method,
            "transaction_status": "completed",
            "transaction_date": payment_date,
            "gateway_response": {
                "transaction_id": f"tx_{payment_id}",
                "status": "approved",
                "gateway": "Stripe"
            }
        }
        transactions_collection.insert_one(transaction_record)

        flash("Payment successfully recorded.", "success")
        return redirect(url_for("payment"))

    return render_template("payment.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    """Display the tenant form page & process data from the creation form."""
    if request.method == "POST":
        new_tenant = {
            "user_first_name": request.form.get("user_first_name"),
            "user_middle_initial": request.form.get("user_middle_initial"),
            "user_last_name": request.form.get("user_last_name"),
            "user_birthday": request.form.get("user_birthday"),
            "user_age": request.form.get("user_age"),
            "user_email": request.form.get("user_email"),
            "user_phone_num": request.form.get("user_phone_num"),
            "current_employer": request.form.get("current_employer"),
            "employer_address": request.form.get("employer_address"),
            "hm_first_name_1": request.form.get("hm_first_name_1"),
            "hm_m_initial_1": request.form.get("hm_m_initial_1"),
            "hm_last_name_1": request.form.get("hm_last_name_1"),
            "hm_birthday_1": request.form.get("hm_birthday_1"),
            "hm_age_1": request.form.get("hm_age_1"),
            "hm_email_1": request.form.get("hm_email_1"),
            "hm_phone_num_1": request.form.get("hm_phone_num_1"),
            "hm_first_name_2": request.form.get("hm_first_name_2"),
            "hm_m_initial_2": request.form.get("hm_m_initial_2"),
            "hm_last_name_2": request.form.get("hm_last_name_2"),
            "hm_birthday_2": request.form.get("hm_birthday_2"),
            "hm_age_2": request.form.get("hm_age_2"),
            "hm_email_2": request.form.get("hm_email_2"),
            "hm_phone_num_2": request.form.get("hm_phone_num_2"),
            "er_first_name_1": request.form.get("er_first_name_1"),
            "er_m_initial_1": request.form.get("er_m_initial_1"),
            "er_last_name_1": request.form.get("er_last_name_1"),
            "er_relationship_1": request.form.get("er_relationship_1"),
            "er_email_1": request.form.get("er_email_1"),
            "er_phone_num_1": request.form.get("er_phone_num_1"),
            "er_first_name_2": request.form.get("er_first_name_2"),
            "er_m_initial_2": request.form.get("er_m_initial_2"),
            "er_last_name_2": request.form.get("er_last_name_2"),
            "er_relationship_2": request.form.get("er_relationship_2"),
            "er_email_2": request.form.get("er_email_2"),
            "er_phone_num_2": request.form.get("er_phone_num_2")
        }
        tenant_insert = mongo.db.tenants.insert_one(new_tenant).inserted_id
        return redirect(url_for("profile", tenant_id=tenant_insert)) 
    return render_template("create_tenant.html")

@app.route("/tenant/<tenant_id>")
def profile(tenant_id):
    """Fetch and display tenant details."""
    tenant_to_show = mongo.db.tenants.find_one({"_id": ObjectId(tenant_id)})

    return render_template("profile.html", tenant=tenant_to_show)

@app.route("/edit/<tenant_id>", methods=["GET", "POST"])
def edit(tenant_id):
    """Shows the edit profile page and accepts a POST request with edited data."""
    if request.method == "POST":
        updated_tenant = {
            "user_first_name": request.form.get("user_first_name"),
            "user_middle_initial": request.form.get("user_middle_initial"),
            "user_last_name": request.form.get("user_last_name"),
            "user_birthday": request.form.get("user_birthday"),
            "user_age": request.form.get("user_age"),
            "user_email": request.form.get("user_email"),
            "user_phone_num": request.form.get("user_phone_num"),
            "current_employer": request.form.get("current_employer"),
            "employer_address": request.form.get("employer_address"),
            "hm_first_name_1": request.form.get("hm_first_name_1"),
            "hm_m_initial_1": request.form.get("hm_m_initial_1"),
            "hm_last_name_1": request.form.get("hm_last_name_1"),
            "hm_birthday_1": request.form.get("hm_birthday_1"),
            "hm_age_1": request.form.get("hm_age_1"),
            "hm_email_1": request.form.get("hm_email_1"),
            "hm_phone_num_1": request.form.get("hm_phone_num_1"),
            "hm_first_name_2": request.form.get("hm_first_name_2"),
            "hm_m_initial_2": request.form.get("hm_m_initial_2"),
            "hm_last_name_2": request.form.get("hm_last_name_2"),
            "hm_birthday_2": request.form.get("hm_birthday_2"),
            "hm_age_2": request.form.get("hm_age_2"),
            "hm_email_2": request.form.get("hm_email_2"),
            "hm_phone_num_2": request.form.get("hm_phone_num_2"),
            "er_first_name_1": request.form.get("er_first_name_1"),
            "er_m_initial_1": request.form.get("er_m_initial_1"),
            "er_last_name_1": request.form.get("er_last_name_1"),
            "er_relationship_1": request.form.get("er_relationship_1"),
            "er_email_1": request.form.get("er_email_1"),
            "er_phone_num_1": request.form.get("er_phone_num_1"),
            "er_first_name_2": request.form.get("er_first_name_2"),
            "er_m_initial_2": request.form.get("er_m_initial_2"),
            "er_last_name_2": request.form.get("er_last_name_2"),
            "er_relationship_2": request.form.get("er_relationship_2"),
            "er_email_2": request.form.get("er_email_2"),
            "er_phone_num_2": request.form.get("er_phone_num_2")
        }
        # Update the tenant in the database
        mongo.db.tenants.update_one(
            { "_id": ObjectId(tenant_id) },
            { "$set": updated_tenant }
        )
        return redirect(url_for("profile", tenant_id=tenant_id))
    else:
        # Retrieve the tenant to edit
        tenant_to_show = mongo.db.tenants.find_one({"_id": ObjectId(tenant_id)})
        return  render_template("edit_profile.html", tenant=tenant_to_show)

        



if __name__ == "__main__":
    app.run(debug=True)
