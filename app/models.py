"""
A collections of "models" (database schema) used throughout the application.
"""

import time
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func


db = SQLAlchemy()


class User(db.Model):
    """
    Represents a User in the application.

    Fields:
        user_id : The not human readable, but unique identifier for a particu-
        lar.
        username : The human readble, but not unique identifier for a particu-
        lar user. (Also used for logging in.)
        password : The password associated with a particular user.
        points : The total amount of points accumulated from solving problems.
    """
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer)

    def __repr__(self):
        # TODO make more descriptive.
        return '<User %r>' % self.username


# TODO Better naming?
class History(db.Model):
    """
    A model representing a particular award at a point in time.
    Fields:
        award_id : Unique identification for an award.
        user_id : User id (represents to recipient of the award.)
        value : The amount the award is worth.
        time_stamp : Time the award was given.
    """
    award_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer)
    # TODO Check approrpriate stirng size.
    time_stamp = db.Column(db.DateTime(timezone=True),
                           server_default=func.now(),
                           nullable=False)

    @property
    def as_javascript(self):
        """
        JSON representation of a particular award.
        """
        return {'award_id': self.award_id,
                'user_id': self.user_id,
                'value': self.value,
                # Convert the datetime object to a string that Javascript can
                # use.
                # See https://stackoverflow.com/a/14469780/667648
                'time_stamp':
                int(time.mktime(self.time_stamp.timetuple())) * 1000}

    def __repr__(self):
        return '<%r awarded to %r at %r' % (
                self.value,
                self.user_id,
                self.time_stamp)


class Problem(db.Model):
    """
    Model for a particular problem. Mostly used for validation of user submiss-
    ion.

    Fields:
        user : Every user is given a particular collection of problems, this is
        the
        data : The contents of the particular problem.
        problem_type : Represents which category the problem belongs too. *No-
        te* available categories are:
            - Alignment
            - Protein
            - Motifs
            - RNA
            - Phylogeny
            - Probability
    """
    user = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(200), nullable=False)
    problem_type = db.Column(db.String(40), nullable=False)


def add_problem(data, user, problem_type):
    """
    Utility function to add problem to database, mostly used to assist in abs-
    tracting away the need to generate a hash for the problem.

    Args:
        data : Problem data.
        user : User solving the problem.
        problem_type : Category the problem belongs to.
    """
    db.session.add(Problem(user=user,
                           data=json.dumps(data),
                           problem_type=problem_type))
    db.session.commit()
