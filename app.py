from flask import Flask, render_template, redirect, request, session, url_for, flash
import helper
import os

# Create a database if it does not exist or if it doesn't have the required schema (it's empty)
if not os.path.exists("database.db") or not os.path.getsize("database.db"):
    helper.create_database()

app = Flask(__name__)
app.secret_key = "0987654321"


@app.route("/")
def index():
    return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        login_type = request.form.get("login_type")
        
        if login_type == "admin":
            admin = helper.fetch_admin(username=email, password=password)
            if admin:
                session["username"] = email
                session["password"] = password
                return redirect(url_for("admin"))
            else:
                flash("Invalid credentials", 'error')
                return redirect("/login")
        elif login_type == "service_professional":
            professional = helper.fetch_professional(email=email, password=password)
            if professional:
                session["username"] = email
                session["password"] = password
                return redirect(url_for("professional_homepage"))
            else:
                flash("Invalid credentials", 'error')
                return redirect("/login")
        elif login_type == "customer":
            customer = helper.fetch_customer(email=email, password=password)
            if customer:
                session["username"] = email
                session["password"] = password
                return redirect(url_for("customer_homepage"))
            else:
                flash("Invalid credentials", 'error')
                return redirect("/login")
    else:
        return render_template("login.html")

@app.route("/customer_signup", methods=["GET", "POST"])
def customer_signup():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        password = request.form.get("password")
        helper.add_customer(fname=fname, lname=lname, address=address, pincode=pincode,
                            contact_number=contact_number, email=email, password=password)
        flash("Successfully signed up!", 'success')
        return redirect("/login")
    else:
        return render_template("customer_signup.html")

@app.route("/professional_signup", methods=["GET", "POST"])
def professional_signup():
    if request.method == "POST":
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        contact_number = request.form.get("contact_number")
        email = request.form.get("email")
        password = request.form.get("password")
        service = request.form.get("service")
        experience = request.form.get("experience")
        description = request.form.get("description")
        helper.add_professional(fname=fname, lname=lname, email=email, password=password,
                                address=address, pincode=pincode, service_id=service,
                                experience=experience, description=description,
                                contact_number=contact_number)
        flash("Successfully signed up!", 'success')
        return redirect("/login")
    else:
        return render_template("professional_signup.html", services=helper.fetch_services())

@app.route("/admin", methods=["GET", "POST"])
@app.route("/admin/<action>/<user_type>/<int:id>", methods=["POST"])
def admin(action=None, user_type=None, id=None):
    if request.method == "POST":
        if action == 'delete':
            if user_type == 'professional' and id:
                helper.delete_professional(id=id)
                return redirect(url_for("admin"))
            elif user_type == 'customer' and id:
                helper.delete_customer(id=id)
                return redirect(url_for("admin"))
            else:
                flash("Process failed!", 'error')
                return redirect(url_for("login"))
        elif action == 'block':
            if user_type == 'professional' and id:
                helper.update_prof_status(status='block', id=id)
                return redirect(url_for("admin"))
            elif user_type == 'customer' and id:
                helper.update_customer_status(status='block', id=id)
                return redirect(url_for("admin"))
            else:
                flash("Process failed!", 'error')
                return redirect(url_for("login"))
        elif action == 'unblock':
            if user_type == 'professional' and id:
                helper.update_prof_status(status='active', id=id)
                return redirect(url_for("admin"))
            elif user_type == 'customer' and id:
                helper.update_customer_status(status='active', id=id)
                return redirect(url_for("admin"))
            else:
                flash("Process failed!", 'error')
                return redirect(url_for("login"))
        elif action == 'accept' and user_type == 'professional' and id:
            helper.update_prof_status(status='active', id=id)
            return redirect(url_for("admin"))
        else:
            flash("Process failed!", 'error')
            return redirect(url_for("login"))
            ...
        ...
    if "username" in session and "password" in session:
        admin = helper.fetch_admin(username=session["username"],
                                    password=session["password"])
        if admin:
            professionals = helper.fetch_professionals()
            customers = helper.fetch_customers()
            services = helper.fetch_services()
            service_requests = helper.fetch_service_requests()
            return render_template("admin.html", professionals=professionals, customers=customers,
                                    services=services, requests=service_requests)
        else:
            flash("Invalid credentials", 'error')
            return redirect(url_for("login"))
    else:
        flash("Invalid credentials", 'error')
        return redirect(url_for("login"))

@app.route("/customer", methods=["GET", "POST"])
def customer_homepage():
    if request.method == "POST":
        customer = helper.fetch_customer(email=session["username"], password=session["password"])
        services = helper.fetch_services()
        packages = helper.available_packages(request.form.get("service_id"))
        service_requests = helper.fetch_service_req(customer_id=session['username'])
        return render_template("customer.html", customer=customer, services=services,
                                requests=service_requests, packages=packages)
    
    if "username" in session and "password" in session:
        customer = helper.fetch_customer(email=session["username"],
                                        password=session["password"])
        if customer and customer['status'] == 'active':
            services = helper.fetch_services()
            service_requests = helper.fetch_service_req(customer_id=session['username'])
            return render_template("customer.html", customer=customer, services=services,
                                requests=service_requests, packages=None)
        elif customer and customer['status'] == 'block':
            flash("You are currently blocked!", 'error')
            return redirect(url_for("login"))
        else:
            flash("Invalid credentials", 'error')
            return redirect(url_for("login"))
    else:
        flash("Invalid credentials", 'error')
        return redirect(url_for("login"))
        
@app.route("/customer/book/<int:prof_id>", methods=['POST'])
def book_service(prof_id):
    helper.book_service(customer_email=session['username'], professional_id=prof_id)
    flash("Service booking done successfully!", 'success')
    return redirect(url_for("customer_homepage"))

@app.route("/customer/close/<int:id>", methods=['POST'])
def close_service(id):
    helper.close_service(id=id, rating=request.form.get('rating'), remarks=request.form.get('remarks'))
    flash("Service closed successfully!", 'success')
    return redirect(url_for("customer_homepage"))

@app.route("/<user_type>/edit", methods=["POST"])
def edit_profile(user_type):
    if user_type == 'professional':
        professional_info = {
            'id': request.form.get("id"),
            'fname': request.form.get("fname"),
            'lname': request.form.get("lname"),
            'address': request.form.get("address"),
            'pincode': request.form.get("pincode"),
            'contact_number': request.form.get("contact_number"),
            'service_id': request.form.get("service"),
            'experience': request.form.get("experience"),
            'description': request.form.get("description"),
        }
        helper.update_profile(user='professional', user_info=professional_info)
        flash("Profile updated successfully!", 'success')
        return redirect(url_for("professional_homepage"))
    elif user_type == 'customer':
        customer_info = {
            'id': request.form.get("id"),
            'fname': request.form.get("fname"),
            'lname': request.form.get("lname"),
            'address': request.form.get("address"),
            'pincode': request.form.get("pincode"),
            'contact_number': request.form.get("contact_number")
        }
        helper.update_profile(user='customer', user_info=customer_info)
        flash("Profile updated successfully!", 'success')
        return redirect(url_for("customer_homepage"))

@app.route("/professional", methods=["GET", "POST"])
def professional_homepage():
    if request.method == "POST":
        helper.accept_reject_service(action=request.form.get('action'), service_id=request.form.get("service_id"))
        if request.form.get("action") == 'accepted':
            flash("Service accepted!", 'success')
        else:
            flash("Service rejected!", 'error')
        return redirect("/professional")
    
    if "username" in session and "password" in session:
        professional = helper.fetch_professional(email=session["username"],
                                                password=session["password"])
        if professional and professional['status'] == 'active':
            requests = helper.fetch_service_req(professional_id=professional['id'])
            return render_template("professional.html", professional=professional, requests=requests,
                                   services=helper.fetch_services())
        elif professional and professional['status'] == None:
            flash("Your request to become a professional is pending!", 'pending')
            return redirect(url_for("login"))
        elif professional and professional['status'] == 'block':
            flash("You are currently blocked!", 'error')
            return redirect(url_for("login"))
        else:
            flash("Invalid credentials", 'error')
            return redirect(url_for("login"))
    else:
        flash("Invalid credentials", 'error')
        return redirect(url_for("login"))

@app.route("/service/<path:subpath>", methods=["POST"])
@app.route("/service/<path:subpath>/<int:id>", methods=["POST"])
def service(subpath, id=None):  
    if subpath == 'add':
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        helper.add_service(name=name, description=description, price=price)
        return redirect(url_for("admin"))
    elif subpath == 'update' and id:
        updated_name = request.form.get("edit_name")
        updated_description = request.form.get("edit_description")
        updated_price = request.form.get("edit_price")
        helper.update_service(id=id, name=updated_name, description=updated_description, price=updated_price)
        return redirect(url_for("admin"))
    elif subpath == 'delete' and id:
        helper.delete_service(id=id)
        return redirect(url_for("admin"))

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect("/login")

"""
When a user do logout, he/she must not be able to go back 
to the same page by pressing the back button of browser.
So to prevent it, I added this after_request decorator
"""
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == "__main__":
    app.run(debug=True)
    