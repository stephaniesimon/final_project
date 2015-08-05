"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Chimes website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    alarm_time = db.Column(db.Time, nullable=True)
    recording_id = db.Column(db.Integer, db.ForeignKey(recordings.recording_id))

    recording = db.relationship("Recording",
                            backref=db.backref("users", order_by=user_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)


class Recording(db.Model):
    """Alarm recording on Chime website."""

    __tablename__ = "recordings"

    recording_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recorder_id = db.Column(db.Integer, nullable=False)
    wav_file = db.Column(db.String(100))

    # change db.String for wav_file once I know what type to use!

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recording recording_id=%s wav_file=%s>" % (self.recording_id, self.wav_file)




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