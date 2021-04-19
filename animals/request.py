import sqlite3
import json

from models import Animal, Location


def get_all_animals():
    with sqlite3.connect('./kennels.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.name location_name,
            l.address location_address
        FROM Animal a
        JOIN Location l
            ON l.id = a.location_id
        """)

        animals = []

        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(
                row['id'],
                row['name'],
                row['breed'],
                row['status'],
                row['location_id'],
                row['customer_id']
            )
            location = Location(
                id = row['location_id'],
                address = row['location_address'],
                name = row['location_name']
            )
            animal.location = location.__dict__
            animals.append(animal.__dict__)

    return json.dumps(animals)



def get_single_animal(id):
    with sqlite3.connect('./kennels.db') as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()
        
        animal = Animal(
            data['id'],
            data['name'],
            data['breed'],
            data['status'],
            data['location_id'],
            data['customer_id']
        )

        return json.dumps(animal.__dict__)



def create_animal(animal):
    max_id = ANIMALS[-1]['id']
    new_id = max_id + 1

    animal['id'] = new_id

    ANIMALS.append(animal)

    return animal

def delete_animal(id):
    with sqlite3.connect('./kennels.db') as conn:
        db_cursor = conn.cursor()

        animal = get_single_animal(id)

        if animal:
            db_cursor.execute("""
            DELETE FROM animal
            where id = ?
            """, (id, ))


def update_animal(id, updated_animal):
    with sqlite3.connect('./kennels.db') as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
        SET
            name = ?,
            breed = ?,
            status= ?,
            location_id = ?,
            customer_id = ?
        where id = ?
        """, (
            updated_animal['name'],
            updated_animal['breed'],
            updated_animal['status'],
            updated_animal['location_id'],
            updated_animal['customer_id'],
            id,
            )
        )

        rows_affected = db_cursor.rowcount

        if rows_affected == 0:
            return False
        else:
            return True
