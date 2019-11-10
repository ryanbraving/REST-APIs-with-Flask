import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help='This field cannot be left blank',
    )
    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            return item, 200
        return {'message': 'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        connnection = sqlite3.connect('data.db')
        cursor = connnection.cursor()

        select_query = 'SELECT * FROM items WHERE name=?'

        result = cursor.execute(select_query, (name,))
        row = result.fetchone()

        connnection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}
        return None

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        insert_query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(insert_query, (item['name'], item['price'], ))

        connection.commit()
        connection.close()

    def post(self, name):
        item = self.find_by_name(name)
        if item:
            return {'message': 'An item with name {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()
        item = {'name': name, "price": data['price']}

        try:
            self.insert(item)
        except:
            return {'message': 'An error occured inserting the item.'}, 500
        
        return item, 201

    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        delete_query = 'DELETE FROM items WHERE name = ?'
        cursor.execute(delete_query, (name,))

        connection.commit()
        connection.close()
        return {'message': 'Item deleted'}

    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        update_query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(update_query, (item['price'], item['name'],))
        
        connection.commit()
        connection.close()

    def put(self, name):

        data = Item.parser.parse_args()

        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}
        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {'message': 'An error occured inserting the item.'}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {'message': 'An error occured updating the item.'}, 500

        return updated_item


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        select_query = 'SELECT * FROM items'
        result = cursor.execute(select_query)
        items=[]
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
       

        connection.close()
        return {"items": items}