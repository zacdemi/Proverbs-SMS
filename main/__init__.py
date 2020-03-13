from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_pyfile("config/config.py")

mongo = PyMongo(app)

from . import routes