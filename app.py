from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash #for hashing and unhashing the password
import sqlite3


app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

@app.route("/")
def start():
    return render_template('index.html') #render_template looks for index.html in templates/ folder and runs that


@app.route('/login', methods = ['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']

    connection = sqlite3.connect('tracker.db')
    cursor = connection.cursor()

    cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
    hashpwd = cursor.fetchone()
    connection.close()
    
    if hashpwd is None:
        return "User doesn't exist! <a href = '/'>Go back</a>"

    id = hashpwd[0]
    pwd = hashpwd[1]
    if check_password_hash(pwd, password):
        session['id'] = id
        session['user'] = username
        return redirect('/dashboard')
    else:
        return "Wrong username or password! <a href = '/'>Go back</a>"

@app.route('/dashboard')
def dashboard():
    return render_template('tracker.html', name=session['user'])


@app.route('/register', methods = ['POST'])
def register():
    data = request.form
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return "Missing fields"
    
    connection = sqlite3.connect('tracker.db')
    cursor = connection.cursor()
    password = generate_password_hash(password)
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()
        return redirect('/')
    except:
        connection.close()
        return "Username already taken! <a href = '/'>Go back</a>"


# @app.route('/forgotpwd', methods = ['POST'])
# def forgotPwd():
#     data = request.form
#     username = data['username']

@app.route('/addHabit')
def addHabit():
    data = request.form()
    habit = data['habit']
    connection = sqlite3.connect('tracker.db')
    cursor = connection.cursor()
    try:
        cursor.execute('INSERT INTO habits (id, habit) VALUES (?, ?)', (session['id'], habit))
        connection.commit()
        connection.close()
        return redirect('/dashboard')
    except:
        connection.close()
        return "Something went wrong! <a href = '/dashboard'>Go back</a>"

if __name__ == '__main__':
    app.run(debug=True)