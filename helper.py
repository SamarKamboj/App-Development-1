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

def add_customer(fname, lname, email, password, address, pincode):
    with get_db() as connection:
        db = connection.cursor()
        db.execute('''INSERT INTO customers (fname, lname, email, password, address, pincode)
            VALUES (?, ?, ?, ?, ?, ?)''',
            (fname, lname, email, password, address, pincode)
        )
        connection.commit()

def fetch_customer(email, password):
    with get_db() as connection:
        db = connection.cursor()
        customer = db.execute("SELECT * FROM customers WHERE email = ? AND password = ?",
                (email, password)).fetchone()
        return customer

def add_professional(fname, lname, email, password, service, experience, address, pincode, description):
    with get_db() as connection:
        db = connection.cursor()
        print(service)
        # service_id = db.execute("SELECT id FROM services WHERE name = ?", (service,)).fetchone()
        if service:
            # service_id = service_id["id"]
            db.execute('''INSERT INTO professionals (fname, lname, email, password, service_id, experience, address, pincode, description, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (fname, lname, email, password, service, experience, address, pincode, description, 'N')
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
        
def update_prof_status(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("UPDATE professionals SET status = 'A' WHERE id = ?", (id,))
        connection.commit()
        
def delete_professional(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("DELETE FROM service_requests WHERE professional_id = ?", (id,))
        db.execute("DELETE FROM professionals WHERE id = ?", (id,))
        connection.commit()

    
def fetch_professionals():
    with get_db() as connection:
        db = connection.cursor()
        professionals = db.execute("SELECT * FROM professionals ORDER BY status, date_created").fetchall()
        return professionals
    
def add_service(name, description, price):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("INSERT INTO services (name, description, price) VALUES (?, ?, ?)",
                   (name, description, price))
        connection.commit()

def delete_service(id):
    with get_db() as connection:
        db = connection.cursor()
        db.execute("DELETE FROM service_requests WHERE service_id = ?", (id,))
        db.execute("DELETE FROM services WHERE id = ?", (id,))
        connection.commit()

def fetch_services():
    with get_db() as connection:
        db = connection.cursor()
        services = db.execute("SELECT * FROM services").fetchall()
        return services
    
def fetch_service_requests():
    with get_db() as connection:
        db = connection.cursor()
        requests = db.execute("SELECT * FROM service_requests").fetchall()
        return requests

