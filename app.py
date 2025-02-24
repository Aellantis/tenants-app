from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
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
maintenance_collection = db.maintenance_requests

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


@app.route("/home")
def home():
    pass


@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email:
            flash("Please enter your email.", "danger")
            return redirect(url_for("login"))

        if not password:
            flash("Please enter your password.", "danger")
            return redirect(url_for("login"))

        tenant = tenants_collection.find_one({"email": email})

        if tenant and check_password_hash(tenant["password"], password):
            session["tenant_id"] = str(tenant["_id"])
            session["tenant_name"] = tenant["name"]
            session["tenant_email"] = tenant["email"]
            session["unit_number"] = tenant["unit_number"]
            flash("Login successful!", "success")
            return redirect(url_for("profile"))
        else:
            flash("Invalid email or password.", "danger")

    return render_template("login.html")

@app.route('/maintenance', methods=['GET', 'POST'])
def maintenance():
    if request.method == 'POST':
        # Extract form data
        reason = request.form.get('reason')
        other_reason = request.form.get('other_reason')
        priority = request.form.get('priority')
        additional = request.form.get('additional')
        schedule_date = request.form.get('schedule_date')
        schedule_time = request.form.get('schedule_time')
        entry_when_no_one_home = request.form.get('entry_when_no_one_home')
        pets_present = request.form.get('pets_present')

        if reason == "Others" and other_reason:
            reason = other_reason

        # Construct the maintenance request document.
        maintenance_request = {
            "reason": reason,
            "priority": priority,
            "additional": additional,
            "schedule_date": schedule_date,
            "schedule_time": schedule_time,
            "entry_when_no_one_home": entry_when_no_one_home,
            "pets_present": pets_present
        }

        # Save to the maintenance collection.
        maintenance_collection.insert_one(maintenance_request)
        flash("Maintenance request submitted successfully.", "success")
        return redirect(url_for('maintenance'))

    # For GET requests, render the maintenance page.
    return render_template('maintenance.html')



@app.route("/delete/<id>", methods=["POST"])
def delete(_id):
    pass


@app.route("/something/<_id>", methods=["GET"])
def another_func(_id):
    pass


if __name__ == "__main__":
    app.run(debug=True)
