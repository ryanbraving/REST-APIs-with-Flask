import sqlite3

class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        connnection = sqlite3.connect('data.db')
        cursor = connnection.cursor()

        select_query = 'SELECT * FROM items WHERE name=?'

        result = cursor.execute(select_query, (name,))
        row = result.fetchone()

        connnection.close()

        if row:
            # return cls(row[0], row[1])
            return cls(*row)
        return None

    def insert(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(insert_query, (self.name, self.price, ))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(update_query, (self.price, self.name,))
        
        connection.commit()
        connection.close()

    