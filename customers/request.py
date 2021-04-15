import sqlite3
import json
from models import Customer

def get_customers_by_email(email):
    with sqlite3.connect('./kennels.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT c.id,
        c.name,
        c.address,
        c.email,
        c.password
        from Customer c
        WHERE c.email = ?
        """, (email, ))

        customers = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            customer = Customer(
                row['id'],
                row['name'],
                row['address'],
                row['email'],
                row['password']
            )
            customers.append(customer.__dict__)

        return json.dumps(customers)
