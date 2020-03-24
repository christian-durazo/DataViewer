import cgi
from flask import Flask, jsonify, render_template, request, session, redirect, url_for, escape, Blueprint
from datetime import datetime
from app.utilities import stringUtils, sendMail
from app.utilities.databaseUtils import mongo
from passlib.hash import sha256_crypt

users = Blueprint('users', __name__)

illegalCharactersForNames = '{}[]<>,./\\()1234567890`~"?!@#$%^&*_+=|:;'


@users.route('/signin', methods=['GET', 'POST'])
def signin():
    if 'username' not in session:

        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = mongo.db.users.find_one_or_404({'username': username})

            # find username/password pair in db
            if user and sha256_crypt.verify(password, user['password']):
                session['username'] = username
                session['role'] = user['role']
            else:
                return render_template('error.html', title="Access Denied")
            return redirect(url_for('users.admin'))
        return render_template('signin.html', title="Sign In", page="signin")
    return redirect(url_for('users.admin'))


@users.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('role', None)
    return redirect(url_for('index'))


@users.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = cgi.escape(request.form['name'])
        username = cgi.escape(request.form['username'])
        email = cgi.escape(request.form['email'])
        password = request.form['password']
        confirmpass = request.form['confirmpass']

        usernameTaken = False
        emailTaken = False
        if mongo.db.users.find_one({'username': username}):
            usernameTaken = True
        if mongo.db.users.find_one({'email': email}):
            emailTaken = True

        if not name or not username or not email or not password or not confirmpass:
            is_error = True
            errormessage = "Something is missing!"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        if '@' not in email:
            is_error = True
            errormessage = "Email Address invalid!"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        elif stringUtils.containsAny(name, illegalCharactersForNames):
            is_error = True
            errormessage = "Name has invalid characters!"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        elif stringUtils.containsAny(username, illegalCharactersForNames):
            is_error = True
            errormessage = "Username has invalid characters!"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        elif password != confirmpass:
            is_error = True
            errormessage = "Password doesn't match"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        elif usernameTaken:
            is_error = True
            errormessage = "Username already taken"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        elif emailTaken:
            is_error = True
            errormessage = "Email already taken"
            return render_template('signup.html', title="Sign Up", page="signup", form=request.form, error=is_error,
                                   errormessage=errormessage)

        else:
            userid = mongo.db.users.insert(
                {'name': name, 'username': username, 'email': email, 'password': sha256_crypt.encrypt(password)})

            subject = "New Editor Request."
            message = name + "(" + email + ") requested to be added as an editor."
            sendMail.send_email("Postmaster", ["postmaster@christiandurazo.com"], "postmaster@christiandurazo.com",
                                subject, message)
            return render_template('signin.html', title="Sign Up - Thank You", page="signup",
                                   content="for your request")
    return render_template('signup.html', title="Sign Up", page="signup")


@users.route("/addUser/<userid>")
def addUser(userid=None):
    if 'username' in session:
        if 'role' in session and session['role'] == 0:

            user = mongo.db.users.find_one_or_404({'_id': userid})

            if user:
                name = user['name']
                email = user['email']

                user = mongo.db.users.find_one_or_404({'_id': userid})

            mongo.db.users.update({'_id': userid}, {"$set": {'role': 1}})

            subject = "You have been added as a user."
            message = name + "(" + email + ") You have been added as an editor for christiandurazo.com. Sign In now at christiandurazo.com/signin"
            sendMail.send_email(name, email, ['postmaster@christiandurazo.com'], subject, message)

            return redirect(url_for('users.admin'))
        return render_template('error.html', title="You do not have the permissions to do this")
    return render_template('error.html', title="You are not Logged In")


@users.route("/admin")
def admin():
    if 'username' in session:
        if 'role' in session and session['role'] == 0:

            userRequests = mongo.db.users.find({'role': None})

            editorRequests = '<ul>'
            for user in userRequests:
                editorRequests += '<li>' + user['name'] + ' : ' + user['email'] + ' <a href="/addUser/' + str(
                    user['_id']) + '">Allow</a> <a href="#">Deny</a></li>'
            editorRequests += '</ul>'
            return render_template('admin.html', title="Editor", content='Logged in as ' + escape(session['username']),
                                   role=session['role'], editorRequests=editorRequests)
        return render_template('error.html', title="You do not have the permissions to do this")
    return render_template('error.html', title="You are not Logged In")
