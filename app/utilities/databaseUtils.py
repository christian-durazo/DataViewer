from flask_pymongo import PyMongo, ObjectId
import urllib.parse
import hashlib

from app import app

app.config['MONGO_DBNAME'] = 'bowlingdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/bowlingdb'
mongo = PyMongo(app)