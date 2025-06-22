#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return "<h1>Bakery GET/POST/PATCH/DELETE API</h1>"

# ---------------------------
# GET all bakeries
@app.route('/bakeries')
def get_bakeries():
    bakeries = Bakery.query.all()
    bakery_list = [bakery.to_dict() for bakery in bakeries]
    return make_response(bakery_list, 200)

# ---------------------------
# GET or PATCH one bakery by ID
@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH'])
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)

    if request.method == 'GET':
        return make_response(bakery.to_dict(), 200)

    elif request.method == 'PATCH':
        name = request.form.get("name")
        if name:
            bakery.name = name
            db.session.commit()
        return make_response(bakery.to_dict(), 200)

# ---------------------------
# GET all baked goods by price (descending)
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    return make_response([good.to_dict() for good in goods], 200)

# ---------------------------
# GET most expensive baked good
@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    return make_response(good.to_dict(), 200)

# ---------------------------
# POST new baked good
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():
    if request.method == 'GET':
        goods = BakedGood.query.all()
        return make_response([good.to_dict() for good in goods], 200)

    elif request.method == 'POST':
        new_good = BakedGood(
            name=request.form.get("name"),
            price=request.form.get("price"),
            bakery_id=request.form.get("bakery_id")
        )
        db.session.add(new_good)
        db.session.commit()
        return make_response(new_good.to_dict(), 201)

# ---------------------------
# DELETE baked good by ID
@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    good = BakedGood.query.get_or_404(id)
    db.session.delete(good)
    db.session.commit()

    return make_response({
        "delete_successful": True,
        "message": f"Baked good with ID {id} deleted."
    }, 200)

# ---------------------------
if __name__ == '__main__':
    app.run(port=5555, debug=True)
