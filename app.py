from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from load_data import load_file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer, db.ForeignKey("order.id"))

    user = relationship("User")
    order = relationship("Order")

    def to_dict(self):
        return {
                'id': self.id,
                'customer_id': self.customer_id,
                'executor_id': self.executor_id
        }


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(500))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    adress = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    executor_id = db.Column(db.Integer)

    user = relationship("User")

    def to_dict(self):
        return {
                'id': self.id,
                'name': self.name,
                'description': self.description,
                'start_date': self.start_date,
                'end_date': self.end_date,
                'adress': self.adress,
                'price': self.price,
                'customer_id': self.customer_id,
                'executor_id': self.executor_id
        }


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(20))

    def to_dict(self):
        return {
                'id': self.id,
                'first_name': self.first_name,
                'last_name': self.last_name,
                'age': self.age,
                'email': self.email,
                'role': self.role,
                'phone': self.phone
        }


db.create_all()


def load_json(file_name, class_name):
    """Функция для заполнения базы данных из json-файлов"""
    json_file = load_file(file_name)

    for record in json_file:
        new_record = class_name(**record)
        db.session.add(new_record)

    db.session.commit()


@app.route("/")
def hi_window():
    """Вьюшка для наполнения главной страницы смысловой нагрузкой"""
    return 'whatsapp nigga?'


@app.route("/users", methods=['GET', 'POST'])
def users():
    """Вьюшка для получения данных про всех пользователей (метод GET)
       Либо для добавления нового пользователя (метод POST)"""

    if request.method == "GET":
        load_json('users.json', User)
        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append(user.to_dict())

        return jsonify(users_list)

    elif request.method == "POST":
        user_data = request.json
        upload_user = User(**user_data)

        db.session.add(upload_user)
        db.session.commit()

        user = User.query.order_by(User.id.desc()).first()

        return jsonify(user.to_dict())


@app.route("/users/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def user_by_id(id):
    """Вьюшка для получения данных про пользователя по его id (метод GET)
       Либо для обновления данных о пользователе (метод PUT)
       Либо для удаления данных о пользователе (метод DELETE)"""

    if request.method == 'GET':
        load_json('users.json', User)
        user = User.query.get(id)
        return jsonify(user.to_dict())

    elif request.method == 'PUT':

        user_data = request.json
        user_update = User.query.get(id)
        user_update.id = user_data['id']
        user_update.first_name = user_data['first_name']
        user_update.last_name = user_data['last_name']
        user_update.age = user_data['age']
        user_update.email = user_data['email']
        user_update.role = user_data['role']
        user_update.phone = user_data['phone']

        db.session.add(user_update)
        db.session.commit()

        user = User.query.get(id)
        return jsonify(user.to_dict())

    elif request.method == 'DELETE':

        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()

        users = User.query.all()
        users_list = []
        for user in users:
            users_list.append(user.to_dict())

        return jsonify(users_list)


@app.route("/orders", methods=['GET', 'POST'])
def orders():
    """Вьюшка для получения данных про все заказы (метод GET)
       Либо для добавления нового заказа (метод POST)"""

    if request.method == "GET":
        load_json('orders.json', Order)
        orders = Order.query.all()
        orders_list = []
        for order in orders:
            orders_list.append(order.to_dict())

        return jsonify(orders_list)

    elif request.method == "POST":
        order_data = request.json
        upload_order = User(**order_data)

        db.session.add(upload_order)
        db.session.commit()

        order = Order.query.order_by(Order.id.desc()).first()

        return jsonify(order.to_dict())


@app.route("/orders/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def order_by_id(id):
    """Вьюшка для получения данных про заказ по его id (метод GET)
       Либо для обновления данных о заказе (метод PUT)
       Либо для удаления заказа (метод DELETE)"""

    if request.method == 'GET':
        load_json('orders.json', Order)
        order = Order.query.get(id)
        return jsonify(order.to_dict())

    elif request.method == 'PUT':
        order_data = request.json
        order_update = User.query.get(id)
        order_update.id = order_data['id']
        order_update.name = order_data['name']
        order_update.description = order_data['description']
        order_update.start_date = order_data['start_date']
        order_update.end_date = order_data['end_date']
        order_update.adress = order_data['adress']
        order_update.price = order_data['price']
        order_update.customer_id = order_data['customer_id']
        order_update.executor_id = order_data['executor_id']

        db.session.add(order_update)
        db.session.commit()

        order = Order.query.get(id)
        return jsonify(order.to_dict())

    elif request.method == 'DELETE':

        order = Order.query.get(id)

        db.session.delete(order)
        db.session.commit()

        orders = order.query.all()
        orders_list = []
        for order in orders:
            orders_list.append(order.to_dict())

        return jsonify(orders_list)


@app.route("/offers", methods=['GET', 'POST'])
def offers():
    """Вьюшка для получения данных про все предложения (метод GET)
       Либо для добавления нового предложения (метод POST)"""

    if request.method == "GET":
        load_json('offers.json', Offer)
        offers = Offer.query.all()
        offers_list = []
        for offer in offers:
            offers_list.append(offer.to_dict())
        return jsonify(offers_list)

    elif request.method == "POST":
        offer_data = request.json
        upload_offer = Offer(**offer_data)

        db.session.add(upload_offer)
        db.session.commit()

        order = Order.query.order_by(Order.id.desc()).first()

        return jsonify(order.to_dict())


@app.route("/offers/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def offer_by_id(id):
    """Вьюшка для получения данных про предложение по его id (метод GET)
       Либо для обновления данных о предложении (метод PUT)
       Либо для удаления предложения (метод DELETE)"""

    if request.method == "GET":
        load_json('offers.json', Offer)
        offer = Offer.query.get(id)
        return jsonify(offer.to_dict())

    elif request.method == 'PUT':
        offer_data = request.json
        offer_update = Offer.query.get(id)
        offer_update.id = offer_data['id']
        offer_update.customer_id = offer_data['customer_id']
        offer_update.executor_id = offer_data['executor_id']

        db.session.add(offer_update)
        db.session.commit()

        offer = Offer.query.get(id)
        return jsonify(offer.to_dict())

    elif request.method == 'DELETE':

        offer = Offer.query.get(id)

        db.session.delete(offer)
        db.session.commit()

        offers = offer.query.all()
        offers_list = []
        for offer in offers:
            offers_list.append(offer.to_dict())

        return jsonify(offers_list)


app.run()
