from flask import Flask, render_template, request, redirect, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash #for hashing and unhashing the password
import sqlite3, calendar
from datetime import datetime


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
    connection = sqlite3.connect('tracker.db')
    cursor = connection.cursor()
    date = datetime.now().strftime("%m")
    query = '''
        SELECT habits.habit_id, habit_log.date
        FROM habits 
        INNER JOIN habit_log ON habits.habit_id = habit_log.habit_id AND habits.id = habit_log.user_id
        WHERE habits.id = ? AND habit_log.date LIKE ?
    '''
    cursor.execute(query, (session['id'],f"%-{date}-%"))
    habitDates = cursor.fetchall()

    cursor.execute('SELECT habit, habit_id FROM habits WHERE id = ?', (session['id'],))
    habits = cursor.fetchall()
    connection.close()

    now = datetime.now()
    days = calendar.monthrange(now.year, now.month)[1]
    return render_template('tracker.html', 
                           name=session['user'], 
                           habitList = habits, 
                           habitDates=habitDates, 
                           numDays = days)


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

@app.route('/addHabit', methods = ['POST'])
def addHabit():
    data = request.form
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

@app.route('/habitCheck', methods = ["POST"])
def habitCheck():
    data = request.get_json()
    
    habit_id = data['habit_id']
    date = data['date']
    check = data['check']

    currdate = datetime.now().strftime("%Y-%m")
    currdate = f"{currdate}-{str(date).zfill(2)}" #zfill will make things like 5 as 05

    conn = sqlite3.connect('tracker.db')
    cursor = conn.cursor()
    if check == 'add':
        cursor.execute('INSERT INTO habit_log (user_id, habit_id, date) VALUES (?,?,?)', (session['id'], habit_id, currdate))        
    else:
        cursor.execute('DELETE FROM habit_log WHERE user_id = ? AND habit_id = ? AND date = ?', (session['id'], habit_id, currdate))
    conn.commit()
    conn.close()

    return jsonify({"msg" : "success"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')