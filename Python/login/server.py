from flask import Flask, request, redirect, render_template, session, flash
# import the Connector function
from mysqlconnection import MySQLConnector
from  flask_bcrypt import Bcrypt
# the 're' module will let us perform some regular expression operations
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# create a regular expression object that we can use run operations on
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app,'login')
# an example of running a query
bcrypt = Bcrypt(app)
app.secret_key = ('secret')

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    errors = False
    

    if len(first_name) < 2:
        flash('Not enough characters')
        errors = True
          
    if len(last_name) < 2:
        flash('Not enough characters')
        errors = True
    
    if len(email) < 1:
        flash('Email is not long enough')
        errors = True
    
    if len(password) < 8:
        flash('Password is not long enough')
        errors = True

    if request.form['confirm'] != password:
        flash('Password does not match')
        errors = True

    if errors == True:
        return redirect('/')

    else:
        email_validate_query = ('SELECT * FROM users WHERE email = :email LIMIT 1')
        email_data = {
            'email': email
        }
        user = mysql.query_db(email_validate_query, email_data)

        if len(user) > 0: 
            flash('Email already assigned')
            return redirect('/')

        else:
            pw_hash = bcrypt.generate_password_hash('password')
            insert_query = 'INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :pw_hash, NOW(), NOW())'
            query_data = { 
                'first_name': request.form['first_name'],
                'last_name': request.form['last_name'],
                'email': request.form['email'],
                'pw_hash': pw_hash
            }

            mysql.query_db(insert_query, query_data)
            return render_template('congratulations.html', first_name = first_name)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    select_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    query_data = {'email': email}
    user = mysql.query_db(select_query, query_data)
    print user

    if len(user) > 0:

        if bcrypt.check_password_hash(user[0]['password'], password):
            session['user_id'] = user[0]['id']
            return render_template('congratulations.html')

        else:
            flash('Email/Password combination does not match')
            return redirect('/')





app.run(debug=True)