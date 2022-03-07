import json

from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
import data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new.db?charset=utf-8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.url_map.strict_slashes = False
db = SQLAlchemy(app)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.Integer)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.Integer)
    end_date = db.Column(db.Integer)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    customer = db.relationship('User', foreign_keys=[customer_id])
    executor = db.relationship('User', foreign_keys=[executor_id])


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User')
    order = db.relationship('Order')


db.drop_all()
db.create_all()

for user in data.users:
    new_user = User(
        id=user['id'],
        first_name=user['first_name'],
        last_name=user['last_name'],
        age=user['age'],
        email=user['email'],
        role=user['role'],
        phone=user['phone'],
    )
    db.session.add(new_user)
db.session.commit()


def structure_data_user(data):
    """
    Serialize implementation
    """
    return {
        "id": data.id,
        "first_name": data.first_name,
        "last_name": data.last_name,
        "age": data.age,
        "email": data.email,
        "role": data.role,
        "phone": data.phone,
    }


def structure_data_order(data):
    """
    Serialize implementation
    """
    return {
        "id": data.id,
        "name": data.name,
        "description": data.description,
        "start_date": data.start_date,
        "end_date": data.end_date,
        "address": data.address,
        "price": data.price,
    }


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    users = [structure_data_user(user) for user in User.query.all()]
    return jsonify(users)


@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_user(id):
    if request.method == 'GET':
        user = structure_data_user(User.query.get(id))
        return jsonify(user)
    elif request.method == 'PUT':
        update_user = json.loads(request.data)
        user = User.query.get(id)
        user.first_name = update_user['first_name']
        user.last_name = update_user['last_name']
        user.age = update_user['age']
        user.email = update_user['email']
        user.role = update_user['role']
        user.phone = update_user['phone']
        db.session.add(user)
        db.session.commit()
        return 'ok'
    elif request.method == 'DELETE':
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return 'ok'
    return 'not found'


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    users = [structure_data_user(user) for user in User.query.all()]
    return jsonify(users)


@app.route('/orders/<id>', methods=['GET', 'PUT', 'DELETE'])
def get_order(id):
    if request.method == 'GET':
        order = structure_data_order(Order.query.get(id))
        return jsonify(order)
    elif request.method == 'PUT':
        updete_order = json.loads(request.data)
        order = Order.query.get(id)
        order.name = updete_order['name']
        order.description = updete_order['description']
        order.start_date = updete_order['start_date']
        order.end_date = updete_order['end_date']
        order.address = updete_order['address']
        order.price = updete_order['price']
        db.session.add(new_user)
        db.session.commit()
        return 'ok'
    elif request.method == 'DELETE':
        order = Order.query.get(id)
        db.session.delete(order)
        db.session.commit()
        return 'ok'
    return 'not found'


if __name__ == '__main__':
    app.run(debug=True)
