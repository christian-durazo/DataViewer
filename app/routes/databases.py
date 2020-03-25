from flask import Flask, jsonify, request, session, redirect, url_for, escape, Blueprint
from flask_pymongo import PyMongo
from app.utilities import stringUtils, sendMail
from app import app

databases = Blueprint('databases', __name__)


@databases.route('/mongo', methods=['POST'])
def mongo():
    app.config['MONGO_URI'] = request.form['databaseuri']
    app.config['MONGO_DBNAME'] = request.form['database']
    mongo = PyMongo(app)

    collection = request.form['collection']
    query = eval(request.form['query'])

    results = mongo.db[collection].find(query, {"_id": 0})
    json_results = []
    json_titles = []
    for result in results:
        for title in result:
            if {'title': title, 'data': title} not in json_titles:
                json_titles.append({'title': title, 'data': title})
        json_results.append(result)
    return jsonify({'data': json_results, 'titles': json_titles})
