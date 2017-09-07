from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
from datetime import datetime
from  flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

app = Flask(__name__)

mysql = MySQLConnector(app,'the_wall')

bcrypt = Bcrypt(app)
app.secret_key = ('secret')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_login', methods=['POST'])
def process_login():
    email = request.form['email']
    password = request.form['password']
    select_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
    query_data = {'email': email}
    user = mysql.query_db(select_query, query_data)
    print user

    if len(user) > 0:

        if bcrypt.check_password_hash(user[0]['password'], password):
            #session['user_id'] = user[0]['id']
            session['user'] = user[0]

            return redirect('/the_wall')

    flash('Email/Password combination does not match')
    return redirect('/')

@app.route('/process_register', methods=['POST'])
def process_register():

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
        return redirect ('/')



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
    user_id = mysql.query_db(insert_query, query_data)
    if int(user_id) == 0:
        flash('Error')
        redirect('/')
    # deleted * and typed out selection, added ':' in id=:id
    insert_query = 'SELECT id, first_name, last_name, email, password, created_At FROM users WHERE id=:id'
    query_data = {'id': user_id}
    results = mysql.query_db(insert_query, query_data)
    session['user'] = results[0]

    return redirect('/the_wall')



@app.route('/the_wall')
def the_wall():
    if not session.has_key('user'):
        flash('Please login')
        redirect('/')
 
    select_query = 'SELECT CONCAT(msg_users.first_name, " ", msg_users.last_name) AS msg_author, messages.id, messages.message, '
    select_query += 'messages.created_at AS msg_created_at, CONCAT(cmt_users.first_name, " ", cmt_users.last_name) AS cmt_author, '
    select_query += 'comments.comment, comments.created_at AS cmt_created_at '
    select_query += 'FROM messages JOIN users AS msg_users ON messages.user_id = msg_users.id '
    select_query += 'LEFT JOIN comments ON messages.id = comments.message_id '
    select_query += 'LEFT JOIN users AS cmt_users ON comments.user_id = cmt_users.id;'

    query_result = mysql.query_db(select_query)
    msg_board = {}

    for row_results in query_result:
        msg_id = row_results['id']
        if not msg_board.has_key(msg_id):
            msg_board[msg_id] = {
                'id' : msg_id,
                'message' : row_results['message'],
                'msg_created_at' : row_results['msg_created_at'],
                'msg_author' : row_results['msg_author'],
                'comments' : []
            }

        if row_results.has_key('cmt_author') and row_results['cmt_author'] != None:
            msg_board[msg_id]['comments'].append({
                'comment' : row_results['comment'],
                'cmt_created_at' : row_results['cmt_created_at'],
                'cmt_author' : row_results['cmt_author']
            })

    # print len(row_results.has_key('cmt_author')) > 0
    # print row_results['cmt_created_at']
    return render_template('the_wall.html', user=session['user'], messages=msg_board.itervalues())

@app.route('/process_message', methods=['POST'])
def process_message():
 
    if not session.has_key('user'):
        return redirect('/')
    
    if len(request.form['message']) < 2:
        flash('Type longer message')
        return redirect('/the_wall')

    else:
        insert_query = 'INSERT INTO messages (user_id, message, created_at, updated_at) VALUES(:user_id, :messages, NOW(), NOW())'
        query_data = {
            'user_id': session['user']['id'],
            'messages': request.form['message']
    }

    message_id = mysql.query_db(insert_query, query_data)

    if int(message_id) == 0:
        flash('Oops! Something went wrong')
    return redirect('/the_wall')

@app.route('/process_comment', methods=['POST'])
def process_comment():
    if not session.has_key('user'):
        return redirect('/')
    if len(request.form['comment']) < 2:
        flash('Type longer comment')
        return redirect('/the_wall')

    else:
        insert_query = 'INSERT INTO comments (user_id, message_id, comment, created_at, updated_at) VALUES(:user_id, :message_id, :comment, NOW(), NOW())'
        query_data = {
            'user_id': session['user']['id'],
            'message_id': request.form['message_id'],
            'comment': request.form['comment']
        }

    comment_id = mysql.query_db(insert_query, query_data)
    if int(comment_id) == 0:
        flash('Oops! Something went wrong')
    return redirect('/the_wall')

@app.route('/logoff')
def logoff():
    if session.has_key('user'):
        session.pop('user')
    return redirect('/')

app.run(debug=True)