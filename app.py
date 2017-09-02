import requests
import random
import string
import hashlib
from functools import wraps

from flask import Flask
from flask import request, jsonify
# from flask import session as session_info
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from json import dumps

from database_setup import Base, User, Beer, Review

engine = create_engine('sqlite:///data.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

app = Flask(__name__)
api = Api(app)


# User stuff
def make_salt():
    """
    Return and string of random
    letters to use as salt.
    """
    return ''.join(random.choice(string.letters) for x in xrange(5))


def make_pw_hash(name, password, salt=None):
    """
    Make password hash with
    username, password, and salt.
    """
    if not salt:
        salt = make_salt()
    my_hash = hashlib.sha256(name + password + salt).hexdigest()
    return salt + ',' + my_hash


def valid_pw(name, password, my_hash):
    """Return true if password is valid"""
    salt = my_hash.split(',')[0]
    return my_hash == make_pw_hash(name, password, salt)


def get_user(username, password):
    user = session.query(User).filter(User.name == username).one()
    if user:
        salt = user.password_hash.split(',')[0]
        password_hash = make_pw_hash(username, password, salt)

        if user.password_hash == password_hash:
            return user


class Users(Resource):
    def get(self):
        # curl -X GET http://localhost:5000/users

        users = session.query(User).all()
        return jsonify(Users=[i.serialize for i in users])

    def put(self):
        # curl -X PUT http://localhost:5000/users -d "name='zayah'&password='cats'"

        username = request.form['name']
        password_hash = make_pw_hash(username, request.form['password'])

        new_user = User(name=username, password_hash=password_hash)
        session.add(new_user)
        session.commit()

        users = session.query(User).all()
        return jsonify(Users=[i.serialize for i in users])


class Beers(Resource):
    def get(self):
        # curl -X GET http://localhost:5000/beers

        beers = session.query(Beer).all()
        return jsonify(Beers=[i.serialize for i in beers])

    def put(self):
        # curl -X PUT http://localhost:5000/beers -d "name='Awesome Beer'&ibu=60&calories=120&abv=4.5&style='Good Style'&brewery_location='Somewhere WI'"
        
        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        if user:
            new_beer = Beer(name=request.form['name'],
                            ibu=request.form['ibu'],
                            calories=request.form['calories'],
                            abv=request.form['abv'],
                            style=request.form['style'],
                            brewery_location=request.form['brewery_location'],
                            user_id=user.id)

            session.add(new_beer)
            session.commit()

            beers = session.query(Beer).all()
            return jsonify(Beers=[i.serialize for i in beers])
        else:
            return "User login error."


class SpecificBeer(Resource):
    # curl -X GET http://localhost:5000/beer/1

    def get(self, beer_id):
        beer = session.query(Beer).get(beer_id)
        return jsonify(Beer=beer.serialize)


class Reviews(Resource):
    def get(self, beer_id):
        # curl -X GET http://localhost:5000/reviews/1

        reviews = session.query(Review).filter(Review.beer_id == beer_id).all()
        return jsonify(Reviews=[i.serialize for i in reviews])

    def put(self, beer_id):
        # curl -X PUT http://localhost:5000/reviews/1 -d "aroma=5&appearance=5&taste=7"

        username = request.form['username']
        password = request.form['password']

        user = get_user(username, password)

        if user:
            aroma = int(request.form['aroma'])
            appearance = int(request.form['appearance'])
            taste = int(request.form['taste'])
            overall = aroma + appearance + taste

            new_review = Review(aroma=aroma,
                                appearance=appearance,
                                taste=taste,
                                overall=overall,
                                beer_id=beer_id,
                                user_id=user.id)

            session.add(new_review)
            session.commit()

            reviews = session.query(Review).filter(Review.beer_id == beer_id).all()
            return jsonify(Reviews=[i.serialize for i in reviews])
        else:
            return "User login error."


api.add_resource(Users, '/users')
api.add_resource(Beers, '/beers')
api.add_resource(SpecificBeer, '/beer/<string:beer_id>')
api.add_resource(Reviews, '/reviews/<string:beer_id>')


if __name__ == '__main__':
    app.run(debug=True)
