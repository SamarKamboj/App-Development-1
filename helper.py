import sqlite3
import sys

def get_db():
    connection = sqlite3.connect("database.db")
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
        return db.execute("SELECT * FROM customers ORDER BY status").fetchall()
    
def delete_customer(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("DELETE FROM customers WHERE id = ?", (id,))
        connection.commit()

def add_professional(fname, lname, email, password, service_id, experience, address, pincode, description, contact_number):
    with get_db() as connection:
        db = connection.cursor()
        if service_id:
            db.execute('''INSERT INTO professionals (fname, lname, email, password, service_id, experience, address, pincode, description, contact_number)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (fname, lname, email, password, service_id, experience, address, pincode, description, contact_number)
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
        return db.execute("SELECT * FROM professionals ORDER BY status, date_created").fetchall()
        
def update_prof_status(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("UPDATE professionals SET status = 'active' WHERE id = ?", (id,))
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
        return db.execute("SELECT * FROM service_requests").fetchall()

