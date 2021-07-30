from flask import Flask, render_template, url_for, jsonify, request, redirect, session

import os
import Data
import sys
sys.path.append('food_dashboard/')
from food_dashboard.analysis import getData


app = Flask(__name__)

UPLOAD_FOLDER = 'data/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(12)

result = None

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/home")
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template("dashboard.html")
    
# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    username = Data.get_data("data/credentials.json").iloc[0]["username"]
    password = Data.get_data("data/credentials.json").iloc[0]["password"]

    if request.method == 'POST':
        if request.form['username'] != username or request.form['password'] != password:
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/word_count', methods=['GET'])
def word_count():
    word = request.args.get('word')
    res = getData(word)
    return jsonify(res)

if __name__ == "__main__":
    # app.secret_key = os.urandom(12)
    app.debug=True
    app.run()
