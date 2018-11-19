from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import time


db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer)

    def __repr__(self):
        # TODO make more descriptive.
        return '<User %r' % self.username


class History(db.Model):
    award_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer)
    # TODO Check approrpriate stirng size.
    time_stamp = db.Column(db.DateTime(timezone=True),
                                       server_default=func.now(),
                                       nullable=False)

    @property
    def as_javascript(self):
        return { 'award_id'   : self.award_id,
                 'user_id'    : self.user_id,
                 'value'      : self.value,
                 # Convert the datetime object to a string that Javascript can
                 # use.
                 # See https://stackoverflow.com/a/14469780/667648
                 'time_stamp' : int(time.mktime(self.time_stamp.timetuple())) * 1000
               }

    def __repr__(self):
        return '<%r awarded to %r at %r' % (self.value, self.user_id, self.time_stamp)
