import sqlite3
import json

from models import Animal

ANIMALS = [
    {
        'id': 1,
        'name': 'Snickers',
        'species': 'Dog',
        'locationId': 1,
        'customerId': 4,
        'status': 'Admitted'
    },
    {
        'id': 2,
        'name': 'Gypsy',
        'species': 'Dog',
        'locationId': 1,
        'customerId': 2,
        'status': 'Admitted'
    },
    {
        'id': 3,
        'name': 'Blue',
        'species': 'Cat',
        'locationId': 2,
        'customerId': 1,
        'status': 'Admitted'
    }
]


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
            a.customer_id
        FROM animal a
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
    animal_index = "not found"

    for index, animal in enumerate(ANIMALS):
        if animal['id'] == id:
            animal_index = index

    if animal_index != "not found":
        ANIMALS.pop(animal_index)
    else:
        pass

def update_animal(updated_animal):
    for index, animal in enumerate(ANIMALS):
        if animal['id'] == updated_animal['id']:
            ANIMALS[index] = updated_animal
            break
