from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def login():
    return render_template('index.html') #render_template looks for index.html in templates/ folder and runs that


if __name__ == '__main__':
    app.run(debug=True)