from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_bcrypt import Bcrypt
import sqlite3
from tacacs_handler import authenticate as tacacs_authenticate

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key' #for encrypting the session data
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    if password != confirm_password: return 'Passwords do not match!'
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    print("HASH: "+password_hash)
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()
    if existing_user:
        conn.close()
        return 'Username already exists!'
    cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password_hash))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

def checkUserData(username,password):
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    if not user: return False
    return bcrypt.check_password_hash(user[2], password)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if checkUserData(username,password):
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return 'Invalid username or password'

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'username' not in session: return redirect(url_for('index'))
    user_id = session['username']
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE username = ?', (user_id,))
    conn.commit()
    conn.close()
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/authenticate', methods=['GET'])
def example_boolean():
    username = request.args.get('username')
    password = request.args.get('password')
    return jsonify({'result': checkUserData(username,password)})

def secondFactor(username,something):
    return True

@app.route('/authenticateTacacs', methods=['GET'])
def authenticateTacacs():
    username = request.args.get('username')
    password = request.args.get('password')
    passhash = bcrypt.generate_password_hash(password).decode('utf-8')
    print("HASH: "+passhash)
    b = tacacs_authenticate(username,password)
    res = False
    if b:
        something = request.args.get('smth')
        res = secondFactor(username,something)
    return jsonify({'result': res})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
