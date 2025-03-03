from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
# from pymongo import MongoClient
# from models.logic import logic_function
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configure MongoDB with Flask-PyMongo
app.config["MONGO_URI"] = os.getenv(
    "MONGO_URI", "mongodb://localhost:27017/tenant_app")
mongo = PyMongo(app)

# Collections
<<<<<<< HEAD
tenants_collection = db.tenants
payments_collection = db.payments
transactions_collection = db.transactions
=======
tenants_collection = mongo.db.tenants
payments_collection = mongo.db.payments
transactions_collection = mongo.db.transactions
maintenance_collection = mongo.db.maintenance_requests
>>>>>>> 1fa1b28 (fix db, fix some flash mess, made login first page you see)

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
<<<<<<< HEAD
    return render_template("home.html")
=======
    return redirect(url_for("login"))


@app.route("/home")
def home():
    tenant = None
    if "tenant_id" in session:
        tenant = mongo.db.tenants_collection.find_one(
            {"_id": ObjectId(session["tenant_id"])})
    return render_template("home.html", tenant=tenant)
>>>>>>> 1fa1b28 (fix db, fix some flash mess, made login first page you see)


@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        # Assuming tenant_id is stored in session
        tenant_id = request.form.get("tenant_id")
        amount = request.form.get("amount")
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
        payment_id = mongo.db.payments_collection.insert_one(
            payment_record).inserted_id

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
        mongo.db.transactions_collection.insert_one(transaction_record)

        flash("Payment successfully recorded.", "success")
        return redirect(url_for("payment"))

    return render_template("payment.html")

@app.route("/profile")
def profile():
    """Display tenant Profile page"""
    return render_template("profile.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    """Display the tenant form page & process data from the creation form."""
    if "tenant_id" not in session:
        flash("You need to register or log in first.", "danger")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        tenant_id = ObjectId(session["tenant_id"]) # Use existing tenant ID

        new_tenant_data = {
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
            "er_phone_num_2": request.form.get("er_phone_num_2"),
            "profile_created": True # Flag to indicate profile creation
        }

        # Update exisiting tenant instad of inserting a new one
        mongo.db.tenants_collection.update_one(
            {"_id": tenant_id},
            {"$set": new_tenant_data}
        )

<<<<<<< HEAD
        return redirect(url_for("detail", tenant_id=tenant_insert)) 
    
=======
        flash("Profile created successfully!", "success")
        return redirect(url_for("detail", tenant_id=session["tenant_id"]))

>>>>>>> ea8c24c (corrected profile route)
    return render_template("create_tenant.html")

@app.route("/tenant/<tenant_id>")
def detail(tenant_id):
    """Fetch and display tenant details."""
    tenant_to_show = mongo.db.tenants_collection.find_one(
        {"_id": ObjectId(tenant_id)})

    if tenant_to_show:
        session["tenant_id"] = tenant_id # Store tenant_id in session

    return render_template("detail_tenant.html", tenant=tenant_to_show)

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
            "er_phone_num_2": request.form.get("er_phone_num_2"),
            "profile_created": True # Ensure the profile is marked as created
        }
        # Update the tenant in the database
<<<<<<< HEAD
        mongo.db.tenants.update_one(
            { "_id": ObjectId(tenant_id) },
            { "$set": updated_tenant }
=======
        mongo.db.tenants_collection.update_one(
            {"_id": ObjectId(tenant_id)},
            {"$set": updated_tenant}
>>>>>>> 1fa1b28 (fix db, fix some flash mess, made login first page you see)
        )
        # Ensure the session is updated with the tenant ID
        session["tenant_id"] = tenant_id
        
        return redirect(url_for("detail", tenant_id=tenant_id))
    else:
        # Retrieve the tenant to edit
<<<<<<< HEAD
        tenant_to_show = mongo.db.tenants.find_one({"_id": ObjectId(tenant_id)})
=======
        tenant_to_show = mongo.db.tenants_collection.find_one(
            {"_id": ObjectId(tenant_id)})
>>>>>>> 1fa1b28 (fix db, fix some flash mess, made login first page you see)

        if tenant_to_show:
            session["tenant_id"] = tenant_id # Store tenant_id in session

        return  render_template("edit_profile.html", tenant=tenant_to_show)

@app.route("/delete/<tenant_id>", methods=["POST"])
def delete(tenant_id):
<<<<<<< HEAD
    mongo.db.tenants.delete_one({"_id": ObjectId(tenant_id)})
    return redirect(url_for("profile"))
=======
    """Delete tenant and clear session only if the tenant exists."""
    tenant = mongo.db.tenants.find_one({"_id": ObjectId(tenant_id)})

    # Remove tenant_id from session
    if tenant:
        mongo.db.tenants_collection.delete_one({"_id": ObjectId(tenant_id)})
        session.pop("tenant_id", None)
        flash("You have deleted your account.", "info")

    return redirect(url_for("create"))


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

        tenant = mongo.db.tenants_collection.find_one({"email": email})

        if tenant and check_password_hash(tenant["password"], password):
            session["tenant_id"] = str(tenant["_id"])
            session["tenant_name"] = tenant["name"]
            session["tenant_email"] = tenant["email"]

            # Ensure user has completed profile creation
            if "profile_created" not in tenant or not tenant["profile_created"]:
                return redirect(url_for("create"))
            
            flash("Login successful!", "success")
            return redirect(url_for("home"))
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
        mongo.db.maintenance_collection.insert_one(maintenance_request)
        flash("Maintenance request submitted successfully.", "success")
        return redirect(url_for('maintenance'))

    # For GET requests, render the maintenance page.
    return render_template('maintenance.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return redirect(url_for("register"))

        # Check if email already exists
        existing_user = mongo.db.tenants.find_one({"email": email})
        if existing_user:
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        # Hash the password before saving
        hashed_password = generate_password_hash(password)

        # Save user to the database
        user_data = {
            "name": name,
            "email": email,
            "password": hashed_password,
            "profile_created": False # Ensure profile creation is required
        }
        result = mongo.db.tenants_collection.insert_one(user_data)

        # Get the inserted document's _id
        tenant_id = str(result.inserted_id)

        # Store user info in the session
        session["tenant_id"] = tenant_id
        session["tenant_name"] = name
        session["tenant_email"] = email

        flash("Registration successful! You can now log in.", "success")
        # return redirect(url_for("login"))
        # Once user registers it takes them to create their profile
        return redirect(url_for("create"))

    return render_template("register.html")


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = tenants_collection.find_one({"email": email})

        if user:
            # Generate a secure token (in a real app, store it in DB and email it)
            reset_token = secrets.token_urlsafe(16)
            mongo.db.tenants_collection.update_one(
                {"email": email},
                {"$set": {"reset_token": reset_token}}
            )

            # TODO: Send an email with the reset token (placeholder)
            flash(
                f"A password reset link has been sent to {email}.", "success")
        else:
            flash("Email not found. Please try again.", "danger")

        return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')
>>>>>>> 1fa1b28 (fix db, fix some flash mess, made login first page you see)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
