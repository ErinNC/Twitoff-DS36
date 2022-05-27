"""SQLAlchemy User and Tweet models for our database"""
from flask_sqlalchemy import SQLAlchemy

# Creates a database object from SQLAlchemy class and connects to it
# Cursor is within DB working behind the scenes
DB = SQLAlchemy()


class User(DB.Model):
    """Creates a User table with SQLAlchemy and defines schema"""
    # User id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # User name column
    username = DB.Column(DB.String, nullable=False)
    # Tweets column comes from DB.backref- working behind the scenes
    # Newest tweet id
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return f"User: {self.username}"

class Tweet(DB.Model):
    """Keeps track of previously posted tweets for each user"""
    # User id column
    id = DB.Column(DB.BigInteger, primary_key=True)
    # Tweet text column
    text = DB.Column(DB.Unicode(300)) # allows for text and links
    # User_id column
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey(
        'user.id'), nullable=False)

    # Adds an attribute to both tables (User and Tweet)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))
    # Create a place to store our word embeddings (vectorization)
    vect = DB.Column(DB.PickleType, nullable=False)

    def __repr__(self):
        return f"Tweet: {self.text}"
