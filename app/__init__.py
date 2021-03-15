from flask import Flask
from flask import render_template
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
import os
import logging

_basedir = os.path.abspath(os.path.dirname(__file__))

logging.basicConfig(filename='app.log', format='%(asctime)s - %(message)s', level=logging.INFO)

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://luizalabs:t3st@lu1z4l4bs@localhost:5432/luizalabs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 't3st@lu1z4l4bs'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

from app.controllers import resources

api.add_resource(resources.Client, '/api/clients', resource_class_kwargs={
    'logging': logging
})