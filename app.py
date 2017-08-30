import requests
from functools import wraps

from flask import Flask
from flask import render_template, request, redirect, url_for, flash
# from flask import session as session_info
from flask_restful import Resource, Api
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from json import dumps

from database_setup import Base, User, Beer, Review

e = create_engine('sqlite:///data.db')

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
	def get(self):
		return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
	app.run(debug=True)
