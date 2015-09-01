"""Models and database functions for Final project."""

from flask_sqlalchemy import SQLAlchemy
import time
import calendar 

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions


class Recording(db.Model):
    """Recording for alarm"""

    __tablename__ = "recordings"

   
    recording_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    question_id = db.Column(db.Integer, db.ForeignKey('questions.question_id'))
    file_path = db.Column(db.String(50))
    file_size = db.Column(db.Integer)
    

    user = db.relationship("User",
                          backref=db.backref("recordings", order_by=recording_id))

    question = db.relationship("Question",
                          backref=db.backref("recordings", order_by=recording_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recording recording_id=%s wav_file=%s>" % (self.recording_id, self.blob)

# 

class User(db.Model):
    """User of Chime website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    
                        

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)



class Category(db.Model):
    """Categories table"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(30), unique=True)
    category_description = db.Column(db.String(300))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category_name=%s>" % (self.category_id, self.category_name)
   

class Question(db.Model):
    """Questions table"""

    __tablename__ = "questions"

    question_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question_text = db.Column(db.String(500))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    category = db.relationship("Category",
                          backref=db.backref("questions", order_by=question_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Question question_id=%s question_text=%s>" % (self.question_id, self.question_text)
   

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chime2.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."