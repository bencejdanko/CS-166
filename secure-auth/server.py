import jwt
import secrets
from flask import (
    render_template, request, g, Flask, jsonify, redirect, url_for, flash
)
import datetime
import sqlite3
import json

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = sqlite3.connect('database.db')
        db.row_factory = sqlite3.Row
        g._database = db
    return db

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    error = None
    try:
        db.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        db.commit()
    except db.IntegrityError:
        error = f'User {username} is already registered.'
        flash(error)
    
    return redirect(url_for("login"))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    secret = request.form['secret']
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()

    if user is None:
        return 'Invalid credentials', 401
    
    if password != user['password']:
        return 'Invalid credentials', 401

    exp_date = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
    refresh_token = secrets.token_hex(16)

    db = get_db()
    existing_token = db.execute('SELECT * FROM refresh_tokens WHERE username = ?', (username,)).fetchone()
    if existing_token:
        db.execute(
            "UPDATE refresh_tokens SET token = ?, expiry = ? WHERE username = ?",
            (refresh_token, exp_date, username)
        )
        old_tokens = None
        if existing_token['old_tokens'] is None:
            old_tokens = []
        else:
            old_tokens = json.loads(existing_token['old_tokens'])
        old_tokens.append(existing_token['token'])
        db.execute("UPDATE refresh_tokens SET old_tokens = ? WHERE username = ?",
            (json.dumps(old_tokens), username)
        )
        db.commit()
    else:
        db.execute(
            "INSERT INTO refresh_tokens (username, token, expiry) VALUES (?, ?, ?)",
            (username, refresh_token, exp_date)
        )
    db.commit()

    response = redirect(url_for('index'))
    response.set_cookie('username', username, httponly=True)
    response.set_cookie('refresh_token', refresh_token, httponly=True)
    return response, 200

@app.route('/secret_access_token', methods=['GET'])
def secret_access_token():
    refresh_token = request.cookies.get('refresh_token')
    username = request.cookies.get('username')
    db = get_db()
    token = db.execute('SELECT * FROM refresh_tokens WHERE token = ? AND username = ?', (refresh_token,username)).fetchone()
    if token is None:
        rows = db.execute('SELECT old_tokens FROM refresh_tokens WHERE username = ?', (username,)).fetchone()
        old_tokens = json.loads(rows['old_tokens'])
        print(refresh_token)
        for token in old_tokens:
            print(token)
        if refresh_token in old_tokens:
            return jsonify({'message': 'Attack suspected! Reseting database access tokens'}), 475
        return 'Invalid token', 401
    if datetime.datetime.utcnow() > datetime.datetime.fromisoformat(token['expiry']):
        return 'Token expired', 401
    
    #token rotation
    exp_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
    new_refresh_token = secrets.token_hex(16)
    db = get_db()
    db.execute(
        "UPDATE refresh_tokens SET token = ?, expiry = ? WHERE token = ?",
        (new_refresh_token, exp_date, refresh_token)
    )

    old_tokens = None
    if token['old_tokens'] is None:
        old_tokens = []
    else:
        old_tokens = json.loads(token['old_tokens'])
    old_tokens.append(token['token'])
    db.execute("UPDATE refresh_tokens SET old_tokens = ? WHERE token = ?",
        (json.dumps(old_tokens), new_refresh_token)
    )
    db.commit()

    exp_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
    secret_access_token = jwt.encode({'username': token['username'], 'exp': exp_date}, 'secret', algorithm='HS256')
    
    response = jsonify({'secret_access_token': secret_access_token})
    response.set_cookie('refresh_token', new_refresh_token, httponly=True)
    response.set_cookie('username', token['username'], httponly=True)
    return response
    

@app.route('/secret', methods=['GET', 'POST'])
def secret():
    secret_access_token = request.headers.get('Authorization')

    if secret_access_token is None:
        print('No token')
        return 'Unauthorized', 401
    try:
        token = jwt.decode(secret_access_token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        print('Expired token')
        return 'Token expired', 401
    except jwt.InvalidTokenError:
        print('Invalid token')
        return 'Invalid token', 401
    if request.method == 'POST':
        secret = request.get_json().get('secret')

        db = get_db()
        existing_secret = db.execute('SELECT * FROM secrets WHERE username = ?', (token['username'],)).fetchone()
        if existing_secret:
            db.execute(
            "UPDATE secrets SET secret = ? WHERE username = ?",
            (secret, token['username'])
            )
        else:
            db.execute(
            "INSERT INTO secrets (username, secret) VALUES (?, ?)",
            (token['username'], secret)
            )
        db.commit()

    db = get_db()
    secret = db.execute('SELECT * FROM secrets WHERE username = ?', (token['username'],)).fetchone()

    return jsonify({'secret': secret['secret']}), 200

@app.route('/cookie', methods=['GET'])
def cookie():
    refresh_token = request.cookies.get('refresh_token')
    return jsonify({'refresh_token': refresh_token}), 200

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

if __name__ == '__main__':
    with app.app_context():
        db = get_db()
        with open('schema.sql') as f:
            db.cursor().executescript(f.read())
    app.run(debug=True)
