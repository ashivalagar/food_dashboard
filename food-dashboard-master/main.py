from flask import Flask, render_template, url_for, jsonify, request, redirect, session
from werkzeug.utils import secure_filename

import os
import requests
import Percentage
import Data
import Interest_by_date
import Meal_of_day


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
        return render_template("home.html")
    
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

@app.route("/ajax", methods = ['POST', 'GET'])
def ajax():
    global result

    print(request)

    term = request.args.get('query')

    insta = Data.get_data('data/instagram.json')
    insta_percent = Percentage.percentage(term, insta, 'text')

    recipe = Data.get_data('data/recipe.json')
    recipe_percent = Percentage.percentage(term, recipe, 'text')

    packaged = Data.get_data('data/packaged.json')
    packaged_percent = Percentage.percentage(term, packaged, 'Name')

    line_insta = Interest_by_date.group_by_date(term, insta)
    line_recipe = Interest_by_date.group_by_date(term, recipe)

    meal = Data.get_data('data/meal.json')
    meal_of_day = Meal_of_day.split_meal(term, meal)
    # print(meal_of_day)

    response = {"percentage": [insta_percent, recipe_percent, packaged_percent],
                "interest": [line_insta, line_recipe],
                "meal": meal_of_day}

    return jsonify(response)

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():

    message = None
    error = None
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('no file')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            error = "No file selected!"
            print('no filename')
        elif file.filename != "instagram.json" and file.filename != "recipe.json" \
            and file.filename != "meal.json" and file.filename != "packaged.json":
            error = "Wrong file name!"
            print('Wrong file name')
        else:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            message = "Save file successfully!"
            print("saved file successfully")

    return render_template('upload.html', message=message, error=error)

if __name__ == "__main__":
    # app.secret_key = os.urandom(12)
    app.run(debug=True)