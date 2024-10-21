import sqlite3
import sys

def get_db():
    connection = sqlite3.connect("database.db")
    connection.execute("PRAGMA foreign_keys = ON")
    connection.row_factory = sqlite3.Row
    return connection

def create_database():
    connection = sqlite3.connect("database.db")
    try:
        path = "schema.sql"
        file = open(path)
    except FileNotFoundError:
        sys.exit(f"{path} not found")
    else:
        connection.executescript(file.read())
        connection.commit()
        connection.close()
        file.close()
        print("Successfully created database\n")
    
def fetch_admin(username, password):
    with get_db() as connection:
        db = connection.cursor()
        admin = db.execute("SELECT * FROM admins WHERE username = ? AND password = ?",
                (username, password)).fetchone()
        return admin

def add_customer(fname, lname, email, password, address, pincode, contact_number):
    with get_db() as connection:
        db = connection.cursor()
        db.execute('''INSERT INTO customers (fname, lname, email, password, address, pincode, contact_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (fname, lname, email, password, address, pincode, contact_number)
        )
        connection.commit()

def fetch_customer(email, password):
    with get_db() as connection:
        db = connection.cursor()
        return db.execute("SELECT * FROM customers WHERE email = ? AND password = ?",
                (email, password)).fetchone()
    
def fetch_customers():
    with get_db() as connection:
        db = connection.cursor()
        return db.execute("SELECT * FROM customers ORDER BY status, id, fname, lname").fetchall()
    
def delete_customer(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("DELETE FROM customers WHERE id = ?", (id,))
        connection.commit()

def add_professional(fname, lname, email, password, service_id, experience, address, pincode, description, contact_number, price):
    with get_db() as connection:
        db = connection.cursor()
        if service_id:
            db.execute('''INSERT INTO professionals (fname, lname, email, password, service_id, service_price, experience, address, pincode, description, contact_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (fname, lname, email, password, service_id, price, experience, address, pincode, description, contact_number)
            )
            connection.commit()
        else:
            print("An error occured while fetching the id of a service\n")

def fetch_professional(email=None, password=None, id=None):
    with get_db() as connection:
        db = connection.cursor()
        if email and password:
            return db.execute("SELECT * FROM professionals WHERE email = ? AND password = ?",
                    (email, password)).fetchone()
        elif id:
            return db.execute("SELECT * FROM professionals WHERE id = ?",
                    (id,)).fetchone()

def fetch_professionals():
    with get_db() as connection:
        db = connection.cursor()
        return db.execute("SELECT * FROM professionals ORDER BY status, id, fname, lname").fetchall()
        
def update_prof_status(status, id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("UPDATE professionals SET status = ? WHERE id = ?", (status, id))
        connection.commit()

def update_customer_status(status, id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("UPDATE customers SET status = ? WHERE id = ?", (status, id))
        connection.commit()
        
def delete_professional(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("DELETE FROM professionals WHERE id = ?", (id,))
        connection.commit()
    
def add_service(name, description, price):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("INSERT INTO services (name, description, price) VALUES (?, ?, ROUND(?, 2))",
                   (name, description, price))
        connection.commit()

def update_service(id, name, description, price):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("UPDATE services SET name = ?, description = ?, price = ? WHERE id = ?",
                   (name, description, price, id))
        connection.commit()

def delete_service(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("DELETE FROM services WHERE id = ?", (id,))
        connection.commit()

def fetch_services():
    with get_db() as connection:
        db = connection.cursor()
        return db.execute("SELECT * FROM services").fetchall()
    
def fetch_service_requests():
    with get_db() as connection:
        db = connection.cursor()
        return db.execute('''SELECT id, service_id, customer_id, professional_id,
                          DATE(datetime(date_of_request), 'localtime') as request_date, TIME(datetime(date_of_request), 'localtime') as request_time,
                          DATE(datetime(date_of_completion), 'localtime') as completion_date, TIME(datetime(date_of_completion), 'localtime') as completion_time,
                          status, rating, remarks FROM service_requests''').fetchall()

def fetch_service_req(customer_id=None, professional_id=None):
    with get_db() as connection:
        db = connection.cursor()
        if customer_id:
            return db.execute('''SELECT id, service_id, customer_id, professional_id,
                            DATE(datetime(date_of_request), 'localtime') as request_date, TIME(datetime(date_of_request), 'localtime') as request_time,
                            DATE(datetime(date_of_completion), 'localtime') as completion_date, TIME(datetime(date_of_completion), 'localtime') as completion_time,
                            status, rating, remarks FROM service_requests WHERE customer_id = (SELECT id FROM customers WHERE email = ?)''', (customer_id,)).fetchall()
        elif professional_id:
            return db.execute('''SELECT sr.id as id, sr.status as request_status, c.fname as customer_fname, c.lname as customer_lname, c.contact_number as customer_number, c.address as customer_address, c.pincode
                            FROM service_requests sr, customers c, professionals p
                            WHERE sr.customer_id = c.id AND sr.professional_id = p.id AND p.id = ?''', (professional_id,)).fetchall()

    
def available_packages(service_id):
    with get_db() as connection:
        db = connection.cursor()
        return db.execute("SELECT * FROM professionals where service_id = ? AND status = 'active'", (service_id,)).fetchall()

def book_service(customer_email, professional_id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute('''
            INSERT INTO service_requests (service_id, customer_id, professional_id)
            VALUES ((SELECT service_id FROM professionals WHERE id = ?),
            (SELECT id FROM customers WHERE email = ?),
            ?)''',
            (professional_id, customer_email, professional_id))
        connection.commit()

def close_service(id, rating, remarks):
    with get_db() as connection:
        db = connection.cursor()
        if not remarks:
            remarks = None
        db.execute("UPDATE service_requests SET status = 'closed', date_of_completion = CURRENT_TIMESTAMP, rating = ?, remarks = ? WHERE id = ?", (rating, remarks, id))

        prof_id = (db.execute("SELECT professional_id FROM service_requests WHERE id = ?", (id,)).fetchone())[0]
        db.execute("UPDATE professionals SET rating = (SELECT ROUND(AVG(rating), 2) FROM service_requests WHERE professional_id = ?) WHERE id = ?", (prof_id, prof_id))
        connection.commit()
    ...

def accept_reject_service(service_id, action):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("UPDATE service_requests SET status = ? WHERE id = ?", (action, service_id))
        connection.commit()

def update_profile(user, user_info):
    with get_db() as connection:
        db = connection.cursor()
        if user == 'professional':
            db.execute('''UPDATE professionals SET fname = ?, lname = ?, address = ?, pincode = ?,
                       contact_number = ?, service_id = ?, service_price = ?, experience = ?, description = ?
                       WHERE id = ?''',
                       (user_info['fname'], user_info['lname'], user_info['address'],
                        user_info['pincode'], user_info['contact_number'],
                        user_info['service_id'], user_info['service_price'],
                        user_info['experience'], user_info['description'], user_info['id']))
        elif user == 'customer':
            db.execute("UPDATE customers SET fname = ?, lname = ?, address = ?, pincode = ?, contact_number = ? WHERE id = ?",
                       (user_info['fname'], user_info['lname'], user_info['address'],
                        user_info['pincode'], user_info['contact_number'], user_info['id']))
        connection.commit()
