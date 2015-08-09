"""Models and database functions for Final project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions


class Recording(db.Model):
    """Recording for alarm"""

    __tablename__ = "recordings"

    file_path = db.Column(db.String(50))
    recording_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recorder_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    alarm_id = db.Column(db.Integer, db. ForeignKey('alarms.alarm_id'))
    

    user = db.relationship("User",
                          backref=db.backref("recordings", order_by=recording_id))

    alarm = db.relationship("Alarm",
                          backref=db.backref("recordings", order_by=recording_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recording recording_id=%s wav_file=%s>" % (self.recording_id, self.blob)

class Alarm(db.Model):
    """Alarm itself"""

    __tablename__ = "alarms"

    alarm_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    alarm_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    set_time = db.Column(db.DateTime)

    user = db.relationship("User",
                          backref=db.backref("alarms", order_by=alarm_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Alarm alarm_id=%s set_time=%s>" % (self.alarm_id, self.set_time)

class User(db.Model):
    """User of Chime website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(80))
    alarm_time = db.Column(db.Time, nullable=True)
                        

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)




   

   

    




##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chime.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."