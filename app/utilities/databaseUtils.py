from flask_pymongo import PyMongo, ObjectId
import urllib.parse
import hashlib

from app import app

app.config['MONGO_DBNAME'] = 'dataViewer'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/dataViewer'
mongo = PyMongo(app)