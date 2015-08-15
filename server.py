
"""Chime server"""

#from jinja2 import StrictUndefined

from flask import Flask, flash, redirect, render_template, request, url_for, session
from  sqlalchemy.sql.expression import func, select
from model import Recording, User, Category, Question, connect_to_db, db
import os
import random
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

    all_questions = db.session.query(Question.question_text).all()
    unformatted_question = random.choice(all_questions)
    # question = [item[0] for item in unformatted_question]



    # all_questions = Question.query.all()
    # # question = all_questions.question_text
    # question = Question.query.filter(Question.question_id == 3).question_text.all()
    


    user = User.query.get(user_id)
    return render_template("user_alarm.html", user=user, question=unformatted_question)


# @app.route("/users")
# def users():
#     """List of users"""

#     return render_template("user_alarm.html", user=user)


@app.route("/record_message")
def record_message():
    """Record message to be played as timer tone"""

    # user = User.query.get(user_id)
    return render_template("make_recording.html")

@app.route('/test2', methods=['POST',])
def save_file():
    """Name and save audio file to S3"""

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename('%s' % int(time.time()) + '.wav')

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        user_id = session["user_id"]
        timer_id= User.query.get(user_id).timers
        new_recording = Recording(file_path=file_path, recorder_user_id=user_id)
        

        # (os.path.abspath("test.wav"))
        db.session.add(new_recording)
        db.session.commit()

    # save audio wav file to S3 bucket

    k = b.new_key(filename)
    k.set_contents_from_file(file)
    return "success!"
    # b.set_acl('public-read')

    # k.get_contents_to_filename(os.path.join('/Users/psimon/Desktop', filename))


@app.route("/recording_play")
def play_recording():
    """User's timer."""
    
    user_id = session["user_id"]
    
    recording = Recording.query.get(recorder_user_id=user_id)

    file_path = Recording.query.get(recording)

    return render_template("recording_play.html", file_path=file_path)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True


    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run()