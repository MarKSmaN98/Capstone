from flask import Flask, session, request, make_response
from flask_restful import Resource
from config import app, db, api
from models import User, Cart, Item, CartItem


#Routes_____________________________________________

class Login(Resource):
    # def get(self):
    #     pass
    def post(self):
        print(request.get_json())
        user = User.query.filter(User.username == request.get_json()['username']).first()
        if user == None:
            resp = make_response({'error':'User Not Found'}, 404)
            return resp
        else:
            session['user_id'] = user.id
            template = {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'age': user.age,
                'email': user.email,
            }
            resp = make_response(template, 200)
            return resp
api.add_resource(Login, '/backlogin')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message':'204: No Content'}, 204
api.add_resource(Logout, '/logout')

class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message': '401: Not Authorized'}, 401
api.add_resource(CheckSession, '/check')           

#Cart
class GetCart(Resource):
    def get(self):
        cartlist = []
        for cart in Cart.query.all():
            template = {
                'id': cart.id,
                'name': cart.name,
                'items' : cart.items,
                'user_id': cart.user_id,
                'paid': cart.paid
            }
            cartlist.append(template)
        resp = make_response(cartlist, 200)
        return resp
    def post(self):
        new = Cart(
            name = request.get_json()['name']
        )
        db.session.add(new)
        try:
            db.session.commit()
            template = {
                'id': template.id,
                'name': template.name,
                'items' : template.items,
                'user_id': template.user_id,
                'paid': template.paid
            }
            resp = make_response(template, 201)
            return resp
        except:
            resp=make_response({'error':'Cart not added'}, 400)
api.add_resource(GetCart, '/cart')

class GetCartById(Resource):
    def get(self, id):
        target = Cart.query.filter(Cart.id == id).first()
        template = {
            'id': target.id,
            'name': target.name,
            'items' : target.items,
            'user_id': target.user_id,
            'paid': target.paid
        }
        resp = make_response(template, 200)
        return resp
    def patch(self, id):
        data = request.get_json()
        target = Cart.query.filter(Cart.id == id).first()
        if target == None:
            resp = make_response({"error":"Cart Not Found"}, 404)
            return resp
        else:
            for attr in data:
                setattr(target, attr, data[attr])
            db.session.add(target)
            db.session.commit()
            template = {
                'id': target.id,
                'name': target.name,
                'items' : target.items,
                'user_id': target.user_id,
                'paid': target.paid
            }
            resp = make_response(template, 200)
            return resp
    def delete(self, id):
        target = Cart.query.filter(Cart.id == id).first()
        if target == None:
            resp = make_response({"error":"Cart Not Found"}, 404)
            return resp
        else:
            db.session.delete(target)
            db.session.commit()
            resp = make_response({}, 204)
            return resp
api.add_resource(GetCartById, '/cart/<int:id>')

#Item

class GetItem(Resource):
    def get(self):
        itemlist = []
        for item in Item.query.all():
            template = {
                'title': item.title,
                'tags': item.tags,
                'price': item.price,
                'img': item.img,
            }
            itemlist.append(template)
        resp = make_response(itemlist, 200)
        return resp
    def post(self):
        new = Item(
            title=request.get_json()['title'],
            tags = request.get_json()['tags'],
            price=request.get_json()['price'],
            img=request.get_json()['img']
        )
        db.session.add(new)
        try:
            db.session.commit()
            resp = make_response(new.to_dict(), 201)
            return resp
        except:
            resp = make_response({'error':'Item not added'}, 400)
            return resp
api.add_resource(GetItem, '/items')

class GetItemById(Resource):
    def get(self, id):
        target = Item.query.filter(Item.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            resp = make_response(target.to_dict(), 200)
            return resp
    def patch(self, id):
        target = Item.query.filter(Item.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            data = request.get_json()
            for attr in data:
                setattr(target, attr, data[attr])
            db.session.add(target)
            db.session.commit()
            resp = make_response(target.to_dict(), 201)
            return resp
    def delete(self, id):
        target = Item.query.filter(Item.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            db.session.delete(target)
            db.session.commit()
            resp = make_response({},204)
            return resp
api.add_resource(GetItemById, '/items/<int:id>')

#CartItem

class GetCartItem(Resource):
    def get(self):
        cartitemlist = []
        for cartItem in CartItem.query.all():
            template = {
                'id': cartItem.id,
                'quantity': cartItem.quantity,
                'item': cartItem.item,
                'cart': cartItem.cart
            }
            cartitemlist.append(template)
        resp = make_response(cartitemlist, 200)
        return resp
    def post(self):
        new = CartItem(
            quantity = request.get_json()['quantity'],
            cart_id = request.get_json()['cart_id'],
            item_id = request.get_json()['item_id']
        )
        db.session.add(new)
        try:
            db.session.commit()
            template = {
                'id': new.id,
                'quantity' :new.quantity,
                'cart_id': new.cart_id,
                'item_id': new.item_id
            }
            resp = make_response(template, 201)
            return resp
        except:
            resp=make_response({'error':'Item not added to cart'}, 400)
api.add_resource(GetCartItem, '/cart_items')

class GetCartItemById(Resource):
    def get(self, id):
        target = CartItem.query.filter(CartItem.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            resp = make_response(target.to_dict(), 200)
            return resp
    def patch(self, id):
        target = CartItem.query.filter(CartItem.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            data = request.get_json()
            for attr in data:
                setattr(target, attr, data[attr])
            db.session.add(target)
            db.session.commit()
            resp = make_response(target.to_dict(), 201)
            return resp
    def delete(self, id):
        target = CartItem.query.filter(CartItem.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found in cart"}, 404)
            return resp
        else:
            db.session.delete(target)
            db.session.commit()
            resp = make_response({},204)
            return resp
api.add_resource(GetCartItemById, '/cart_items/<int:id>')

#user

class GetUser(Resource):
    def get(self):
        userlist = []
        for user in User.query.all():
            template = {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'age': user.age,
                'email': user.email,
                'password': user.password
            }
            userlist.append(template)
        resp = make_response(userlist, 200)
        return resp
    def post(self):
        new = CartItem(
            name = request.get_json()['name'],
            age = request.get_json()['age'],
            username = request.get_json()['username'],
            email = request.get_json()['email'],
            password = request.get_json()['password']
        )
        db.session.add(new)
        try:
            db.session.commit()
            template = {
                'id': new.id,
                'name' :new.name,
                'username': new.username,
                'age': new.age,
                'email': new.email,
                'password': new.password
            }
            resp = make_response(template, 201)
            return resp
        except:
            resp=make_response({'error':'User not added'}, 400)
api.add_resource(GetUser, '/users')

class GetUserByID(Resource):
    def get(self, id):
        target = User.query.filter(User.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            template = {
                'id': target.id,
                'name' :target.name,
                'username': target.username,
                'age': target.age,
                'email': target.email,
                'password': target.password,
                'carts': target.user_carts
            }
            resp = make_response(template, 200)
            return resp
    def patch(self, id):
        target = User.query.filter(User.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found"}, 404)
            return resp
        else:
            data = request.get_json()
            for attr in data:
                setattr(target, attr, data[attr])
            db.session.add(target)
            db.session.commit()
            resp = make_response(target.to_dict(), 201)
            return resp
    def delete(self, id):
        target = User.query.filter(User.id == id).first()
        if target == None:
            resp = make_response({"error":"Item not found in cart"}, 404)
            return resp
        else:
            db.session.delete(target)
            db.session.commit()
            resp = make_response({},204)
            return resp
api.add_resource(GetUserByID, '/users/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)