from flask import Flask, render_template, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash #for hashing and unhashing the password
import sqlite3


app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html') #render_template looks for index.html in templates/ folder and runs that

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
        return "Username already taken! <a>Go back</a>"


@app.route('/forgotpwd', methods = ['POST'])
def forgotPwd():
    data = request.get_json()
    mail = data['email']

if __name__ == '__main__':
    app.run(debug=True)