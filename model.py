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

   
    recording_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    recorder_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    timer_id = db.Column(db.Integer, db. ForeignKey('timers.timer_id'))
    file_path = db.Column(db.String(50))
    

    user = db.relationship("User",
                          backref=db.backref("recordings", order_by=recording_id))

    timer = db.relationship("Timer",
                          backref=db.backref("recordings", order_by=recording_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Recording recording_id=%s wav_file=%s>" % (self.recording_id, self.blob)

# 

class User(db.Model):
    """User of Chime website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(80))
    
                        

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id, self.email)



class Timer(db.Model):
    """Timer table"""

    __tablename__ = "timers"

    timer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    timer_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    timer_time = db.Column(db.Integer)

    user = db.relationship("User",
                          backref=db.backref("timers", order_by=timer_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Timer timer_id=%s set_time=%s>" % (self.timer_id, self.set_time)
   

   

    # class Alarm(db.Model):
#     """Alarm itself"""

#     __tablename__ = "alarms"

#     alarm_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     alarm_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
#     set_time = db.Column(db.DateTime)

#     user = db.relationship("User",
#                           backref=db.backref("alarms", order_by=alarm_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Alarm alarm_id=%s set_time=%s>" % (self.alarm_id, self.set_time)




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