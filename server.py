
"""Chime server"""

#from jinja2 import StrictUndefined

from cStringIO import StringIO
from flask import Flask, flash, redirect, jsonify, render_template, request, url_for, session
from  sqlalchemy.sql.expression import func, select
from model import Recording, User, Category, Question, connect_to_db, db
import os
import random
import csv
import sys
import sqlite3
from werkzeug.utils import secure_filename

import boto
from boto.s3.key import Key
import time


# s3 connection and bucket definition
c = boto.connect_s3()
b = c.get_bucket('boto-demo-1438909409')


UPLOAD_FOLDER = 'https://s3.amazonaws.com/boto-demo-1438909409'
ALLOWED_EXTENSIONS = set(['wav'])

# from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "ABC"



#app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")

@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    return render_template("register.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]
    first_name = request.form["first_name"]

    new_user = User(email=email, password=password, first_name=first_name)
    

    db.session.add(new_user)
    db.session.commit()
    
    session["user_id"] = new_user.user_id
    flash("User %s added." % first_name)

    return redirect("/users/%s" % new_user.user_id)

    # return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id


    flash("Logged in")
    return redirect("users/%s" % user.user_id)


@app.route("/users/<int:user_id>", methods=['GET'])
def user_profile(user_id):
    """User's timer profile"""


    all_questions = db.session.query(Question.question_text, Question.question_id).all()
    unformatted_question = random.choice(all_questions)
    question_text = str(unformatted_question[0])
    question_id = unformatted_question[1]
    user = User.query.get(user_id)
    session["question_id"] = question_id

    return render_template("user_alarm.html", user=user, question=question_text, question_id=question_id)

@app.route("/save_recording", methods=['POST',])
def save_file():
    """Name and save audio file to S3"""

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename('%s' % int(time.time()) + '.wav')

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        user_id = session["user_id"] 
        question_id = session ["question_id"]
        new_recording = Recording(file_path=file_path, user_id=user_id, question_id=question_id)
        

        db.session.add(new_recording)
        db.session.commit()

    k = b.new_key(filename)
    k.set_contents_from_file(file)
    return "success!"


@app.route("/visualization_process.csv", methods=['GET',])
def visualization_process():
    """Process d3 visualization of user's answers"""
  
    # con = sqlite3.connect('chime2.db')

    #outfile = open('seed_data/recordings.csv', 'wb')
    outfile = StringIO()
    outcsv = csv.writer(outfile)

    # cursor = con.execute("""
    #  Select r.user_id, 
    #         r.question_id, 
    #         r.file_path, 
    #         q.question_text 
    # from recordings as r join questions as q on r.question_id=q.question_id
    # WHERE r.user_id = ?""", [THEUSERID])

    results = db.session.query(Recording.user_id,
                               Recording.question_id,
                               Recording.file_path,
                               Question.question_text).join(Question).filter(Recording.user_id == session['user_id'])
        
    # dump rows
    # outcsv.writerow(["foo","bar","zork"])
    # outcsv.writerows(cursor.fetchall())
    outcsv.writerows(results.all())

    outfile.seek(0)
    return outfile.read()

    #outfile.close()

    #return redirect("/visualize")


# @app.route("/recordings.json")
# def recordings_json():
#     test_dict = []
#     with open('seed_data/recordings.csv', 'rb') as csvfile:
#         reader = csv.reader(csvfile, delimiter=',', quotechar='|')
#         for row in reader:
#             test_dict.append(row)

#     return jsonify(data_list=test_dict)


@app.route("/visualize")
def visualize_data():
    """d3 visualization of user's answers"""


    return render_template("visualization.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True


    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)


    app.run()