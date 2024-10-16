from flask import Flask, render_template, redirect, request, session, url_for
import helper
import os

# Create a database if it does not exist or if it doesn't have the required schema (empty)
if not os.path.exists("database.db") or not os.path.getsize("database.db"):
    helper.create_database()

app = Flask(__name__)
app.secret_key = "0987654321"

def get_admin():
    if "username" in session and "password" in session:
        return helper.fetch_admin(username=session["username"],
                                    password=session["password"])
    else:
        return None


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
                return redirect("/login")
        elif login_type == "service_professional":
            professional = helper.fetch_professional(email=email, password=password)
            if professional:
                session["username"] = email
                session["password"] = password
                return redirect(url_for("professional_homepage"))
            else:
                return redirect("/login")
        elif login_type == "customer":
            customer = helper.fetch_customer(email=email, password=password)
            if customer:
                session["username"] = email
                session["password"] = password
                return redirect(url_for("customer_homepage"))
            else:
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
        return redirect("/login")
    else:
        return render_template("professional_signup.html", services=helper.fetch_services())

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        ...
    else:
        if get_admin():
            professionals = helper.fetch_professionals()
            customers = helper.fetch_customers()
            services = helper.fetch_services()
            service_requests = helper.fetch_service_requests()
            return render_template("admin.html", professionals=professionals, customers=customers,
                                   services=services, requests=service_requests)
        else:
            return redirect(url_for("login"))
        
@app.route("/admin/search", methods=["GET", "POST"])
def admin_search():
    if request.method == "POST":
        ...
    else:
        return render_template("admin_search.html")
    ...

@app.route("/customer", methods=["GET", "POST"])
def customer_homepage():
    if request.method == "POST":
        customer = helper.fetch_customer(email=session["username"], password=session["password"])
        services = helper.fetch_services()
        packages = helper.available_packages(request.form.get("service_id"))
        service_requests = helper.fetch_service_req(customer_id=session['username'])
        return render_template("customer.html", customer=customer, services=services,
                                requests=service_requests, packages=packages)
        ...
    else:
        if "username" in session and "password" in session:
            customer = helper.fetch_customer(email=session["username"],
                                            password=session["password"])
        else:
            customer = None

        if customer:
            services = helper.fetch_services()
            service_requests = helper.fetch_service_req(customer_id=session['username'])
            return render_template("customer.html", customer=customer, services=services,
                                   requests=service_requests, packages=None)
        else:
            return redirect(url_for("login"))
        
@app.route("/book/<int:prof_id>", methods=['POST'])
def book_service(prof_id):
    helper.book_service(customer_email=session['username'], professional_id=prof_id)
    return redirect(url_for("customer_homepage"))

@app.route("/close/<int:id>", methods=['POST'])
def close_service(id):
    helper.close_service(id=id, rating=request.form.get('rating'), remarks=request.form.get('remarks'))
    return redirect(url_for("customer_homepage"))

# @app.route("/professional/<int:service_id>", methods=["POST"])
@app.route("/professional", methods=["GET", "POST"])
def professional_homepage(service_id=None):
    if request.method == "POST":
        helper.accept_reject_service(action=request.form.get('action'), service_id=request.form.get("service_id"))
        return redirect("/professional")
    else:
        if "username" in session and "password" in session:
            professional = helper.fetch_professional(email=session["username"],
                                                    password=session["password"])
        else:
            professional = None

        if professional:
            requests = helper.fetch_service_req(professional_id=professional['id'])
            return render_template("professional.html", professional=professional, requests=requests)
        else:
            return redirect(url_for("login"))

@app.route("/service/<path:subpath>", methods=["POST"])
@app.route("/service/<path:subpath>/<int:id>", methods=["POST"])
def service(subpath, id=None):  
    if get_admin():
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
    else:
        return redirect(url_for("login"))

@app.route("/accept_reject/<int:id>", methods=["GET", "POST"])
def accept_reject(id):
    if get_admin():
        if request.form.get("action") == "accept":
            helper.update_prof_status(status='active', id=id)
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("delete", user='professional', id=id))
    else:
        return redirect(url_for("login"))
    
@app.route("/block_unblock/<user>/<int:id>", methods=["GET", "POST"])
def block_unblock(user, id):    
    if get_admin():
        if user == 'professional' and id:
            if request.form.get("action") == 'block':
                helper.update_prof_status(status='block', id=id)
                return redirect(url_for("admin"))
            elif request.form.get("action") == 'unblock':
                helper.update_prof_status(status='active', id=id)
                return redirect(url_for("admin"))
            elif request.form.get("action") == 'remove':
                return redirect(url_for("delete", user='professional', id=id))
            else:
                return redirect(url_for("admin"))
        elif user == 'customer' and id:
            if request.form.get("action") == 'block':
                helper.update_customer_status(status='block', id=id)
                return redirect(url_for("admin"))
            elif request.form.get("action") == 'unblock':
                helper.update_customer_status(status='active', id=id)
                return redirect(url_for("admin"))
            elif request.form.get("action") == 'remove':
                return redirect(url_for("delete", user='customer', id=id))
            else:
                return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))

@app.route("/delete/<user>/<int:id>", methods=["GET", "POST"])
def delete(user, id):    
    if get_admin():
        if user == 'professional' and id:
            helper.delete_professional(id=id)
            return redirect(url_for("admin"))
        elif user == 'customer' and id:
            helper.delete_customer(id=id)
            return redirect(url_for("admin"))
    else:
        return redirect(url_for("login"))

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
    """
    Add headers to both force a fresh reload and prevent browser caching
    of sensitive pages.
    """
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response


if __name__ == "__main__":
    app.run(
        debug=True
    )