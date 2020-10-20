from flask import Flask, jsonify, request, session, redirect, url_for, escape, Blueprint
from flask_mysqldb import MySQL
from flask_mysql import MySql
import ast
from app.utilities import stringUtils, sendMail
from app import app

databases = Blueprint('databases', __name__)


@databases.route('/mongo', methods=['POST'])
def mongo():
    app.config['MONGO_URI'] = request.form['databaseuri']
    app.config['MONGO_DBNAME'] = request.form['database']
    mongo = PyMongo(app)

    collection = request.form['collection']
    query = ast.literal_eval(request.form['query'])

    results = mongo.db[collection].find(query, {"_id": 0})
    json_results = []
    json_titles = []
    for result in results:
        for title in result:
            if {'title': title, 'data': title} not in json_titles:
                json_titles.append({'title': title, 'data': title})
        json_results.append(result)
    return jsonify({'data': json_results, 'titles': json_titles})


@databases.route('/mysql', methods=['POST'])
def mysql():
    app.config['MYSQL_HOST'] = request.form['databaseuri']
    app.config['MYSQL_USER'] = request.form['user']
    app.config['MYSQL_PASSWORD'] = request.form['passwd']
    app.config['MYSQL_DB'] = request.form['database']

    mysql = MySQL(app)
    
    query = ast.literal_eval(request.form['query'])
    
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
        
    json_results = []
    json_titles = []
    for result in results:
        row = []
        for title in result:
            if {'title': title, 'data': title} not in json_titles:
                json_titles.append({'title': title, 'data': title})
            row.append({'title': title, 'data': result[title]}
        json_results.append(row)
    return jsonify({'data': json_results, 'titles': json_titles})
    
