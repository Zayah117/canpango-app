import requests
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


class Beers(Resource):
	def get(self):
		beers = session.query(Beer).all()
		return jsonify(Beers=[i.serialize for i in beers])

	def put(self):
		# put('http://localhost:5000/beers', data={'name': 'beer name', 'ibu': 60, 'calories': 120, 'abv': 4.5, 'style': 'good beer', 'brewery_location': 'Somewhere - IN'}).json()

		new_beer = Beer(name=request.form['name'],
				ibu=request.form['ibu'],
				calories=request.form['calories'],
				abv=request.form['abv'],
				style=request.form['style'],
				brewery_location=request.form['brewery_location'])

		session.add(new_beer)
		session.commit()

		beers = session.query(Beer).all()
		return jsonify(Beers=[i.serialize for i in beers])


class SpecificBeer(Resource):
        def get(self, beer_id):
		beer = session.query(Beer).get(beer_id)
		return jsonify(Beer=beer.serialize)


api.add_resource(Beers, '/beers')
api.add_resource(SpecificBeer, '/beer/<string:beer_id>')


if __name__ == '__main__':
	app.run(debug=True)
