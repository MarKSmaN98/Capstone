from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
from datetime import datetime

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    serialize_rules = ('-user_carts', '-cart.cart_user')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)    
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    type = db.Column(db.Integer, nullable=False, default=0) #0 is normal user, 1 is seller
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_carts = db.relationship('Cart', backref='user', lazy=True)

class Cart(db.Model, SerializerMixin):
    __tablename__ = 'carts'
    serialize_rules = ('-items.cart', '-cart.cart_items', '-cart.cart_user', '-cart_items.cart')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    items = association_proxy('cart_items', 'item')
    cart_items = db.relationship('CartItem', backref='cart')

class Item (db.Model, SerializerMixin):
    __tablename__ = 'items'
    serialize_rules = ('-cart_items.cart', '-cart_items', '-cart_items.item', '-cart.items')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=False) #eventually another table probably
    price = db.Column(db.Float, nullable=False)
    img = db.Column(db.String, nullable=False) #another table?
    cart = association_proxy('cart_items', 'cart')
    cart_items = db.relationship('CartItem', backref='item')

class CartItem(db.Model, SerializerMixin):
    __tablename__ = 'cart_items'
    serialize_rules = ('-cart.cart_items', '-item.cart_items')

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    cart_id = db.Column(db.Integer, db.ForeignKey('carts.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))


