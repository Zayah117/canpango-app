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

class HelloWorld(Resource):
	def get(self):
		return {'hello': 'world'}

class Beers(Resource):
	def get(self):
		beers = session.query(Beer).all()
		return jsonify(Beers=[i.serialize for i in beers])

class SingleBeer(Resource):
        def get(self, beer_id):
		beer = session.query(Beer).get(beer_id)
		return jsonify(Beer=beer.serialize)

api.add_resource(HelloWorld, '/')
api.add_resource(Beers, '/beers')
api.add_resource(SingleBeer, '/beer/<string:beer_id>')

if __name__ == '__main__':
	app.run(debug=True)
