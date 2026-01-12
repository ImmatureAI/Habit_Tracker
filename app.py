from flask import Flask, render_template, request, jsonify, session


app = Flask(__name__)

@app.route("/")
def start():
    return render_template('index.html') #render_template looks for index.html in templates/ folder and runs that

@app.route('/register', methods = ['POST'])
def register():
    data = request.form
    mail = data.get('email')
    password = data.get('password')

@app.route('/forgotpwd', methods = ['POST'])
def forgotPwd():
    data = request.get_json()
    mail = data['email']

if __name__ == '__main__':
    app.run(debug=True)