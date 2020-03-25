import os
from datetime import datetime

from flask import render_template, request

from app import app
from app.utilities import stringUtils, sendMail
from .users import users
from .databases import databases

UPLOAD_FOLDER = os.path.dirname(__file__) + '/static/images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(users)
app.register_blueprint(databases)

file = open("app/key.txt")
app.secret_key = file.readline()
file.close()

illegalCharactersForNames = '{}[]<>,./\\()1234567890`~"?!@#$%^&*_+=|:;'


@app.route('/')
def index():
	user = "Christian Durazo"  # TODO add user auth
	return render_template('index.html', user=user)


@app.route('/charts')
def charts():
	return render_template('charts.html')


@app.route('/layout-sidenav-light')
def layout_sidenav_light():
	return render_template('layout-sidenav-light.html')


@app.route('/layout-static')
def layout_static():
	return render_template('layout-static.html')


@app.route('/login')
def login():
	return render_template('login.html')


@app.route('/password')
def password():
	return render_template('password.html')


@app.route('/register')
def register():
	return render_template('register.html')


@app.route('/tables')
def tables():
	return render_template('tables.html')


@app.route('/error')
def error():
	return render_template('404.html')


@app.errorhandler(500)
def server_error():
	return render_template('500.html')


@app.errorhandler(401)
def unauthorized():
	return render_template('401.html'), 404


@app.errorhandler(404)
def page_not_found():
	return render_template('404.html'), 404


@app.context_processor
def inject_now():
	return {'now': datetime.utcnow()}
