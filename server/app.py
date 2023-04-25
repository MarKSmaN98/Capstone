from flask import Flask, session, request, make_response
from flask_restful import Resource
from config import app, db, api
from models import User, Cart, Item, CartItem


#Routes_____________________________________________

class Login(Resource):
    # def get(self):
    #     pass
    def post(self):
        user = User.query.filter(User.username == request.get_json()['username']).first()
        session['user_id'] = user.id
        return user.to_dict()
api.add_resource(Login, '/login')

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
        


if __name__ == '__main__':
    app.run(port=5555, debug=True)