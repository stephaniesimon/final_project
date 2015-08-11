
"""Chime server"""

#from jinja2 import StrictUndefined

from flask import Flask, flash, redirect, render_template, request, url_for, session
from model import Recording, User, Alarm, connect_to_db, db
import os
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

    # wav_file = request.form.get

    return render_template("index.html")



@app.route('/test2', methods=['POST',])
def save_file():
    """Name and save audio file to S3"""

    if request.method == 'POST':
        # file = request.files.get('file')
        file = request.files['file']

        #if file:
        # filename = secure_filename('%s' % int(time.time()) + '.wav')
        filename = secure_filename('%s' % int(time.time()) + '.wav')

        # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # new_recording = Recording(file_path=(os.path.abspath(filename)))

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_recording = Recording(file_path=file_path)
        print file_path

        # (os.path.abspath("test.wav"))
        db.session.add(new_recording)
        db.session.commit()

    # save audio wav file to S3 bucket

    k = b.new_key(filename)
    k.set_contents_from_file(file)
    # b.set_acl('public-read')

    # create k which is directed to the aws filepath you want, retrieve from db.
        # b = https://s3.amazonaws.com/boto-demo-1438909409/
        # k = b + 1438993622.wav

        # will need to recreate the k value, by getting 1438993622.wav
           # k = b + 1438993622.wav     

    # go to k, get contents, and place in '/Users/psimon/Desktop' + 1438993622.wav
    # k.get_contents_to_filename(os.path.join('/Users/psimon/Desktop', filename))
    

    # flash('You were successfully logged in')
    # return redirect('/users/<int:user_id>')

    return "success!"




# @app.route('/')
# def get_audio():
#     """Accessing audio file"""

    # recording = audio

# @app.route('/alarm')
# def playing_with_alarm():
#     """Playing with alarm"""

#     return render_template("clock.html")

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
    # user = User.query.filter_by(email=email).first()

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

    # Get form variables
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No such user")
        return redirect("/login")

    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    # session["user_id"] = user.user_id

    # flash("Logged in")
    return redirect("users/%s" % user.user_id)


@app.route("/users/<int:user_id>", methods=['GET'])
def user_profile(user_id):
    """User's alarm profile"""

    user = User.query.get(user_id)
    return render_template("user_alarm.html", user=user)

    # When user clicks "set alarm", goes to set_alarm route

@app.route("/users/<int:user_id>", methods=['POST'])
def alarm_set_process(user_id):
    """Set alarm for that profile"""



    user = User.query.get(user_id)
    
    return redirect("users/%s/set_alarm" % user.user_id)
        


@app.route("/users/set_alarm")
def user_alarm(user_id):
    """Set alarm"""

    user = User.query.get(user_id)
    return render_template("set_alarm.html")

@app.route("/users/<int:user_id>/record")
def record_message(user_id):
    """Record message to be played as alarm tone"""

    # user = User.query.get(user_id)
    # return render_template("set_alarm.html")

# @app.route("/set alarm/<int:user_id>")
# def play_recording():
#     """User's alarm."""

#     user = query.get(user_id)

#     file_path = User.query.get(user).file_path

#     return redirect("users/%s" % user.user_id)

#     return render_template("recording_play.html", file_path=file_path)

# @app.route("/recording_play/<int:user_id>")
# def play_recording():
#     """User's alarm."""


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    #DebugToolbarExtension(app)

    app.run()