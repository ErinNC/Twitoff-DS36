"""SQLAlchemy User and Tweet models for our database"""
from flask_sqlalchemy import SQLAlchemy

# Creates a database object from SQLAlchemy class and connects to it
# Cursor is within DB working behind the scenes
DB = SQLAlchemy()


class User(DB.Model):
    """Creates a User table with SQLAlchemy"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # name column
    username = DB.Column(DB.String, nullable=False)
    # tweets column comes from DB.backref- working behind the scenes

    def __repr__(self):
        return f"User: {self.username}"

class Tweet(DB.Model):
    """Keeps track of tweets for each user"""
    # id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # text column
    text = DB.Column(DB.Unicode(300)) # allows for text and links
    # user_id column
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)
    # user
    # Going to add an attribute to both tables (User and Tweet)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return f"Tweet: {self.text}"