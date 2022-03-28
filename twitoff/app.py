'''Module docstring'''
from re import DEBUG
from flask import Flask, render_template
from .models import DB, User, Tweet

def create_app():
    '''Function to call from __init__.py to auto initialize our app'''

    # Initialize our app
    app  = Flask(__name__)

    # Database configuration- tells our app where to find DB
    # "registering" our database with the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    # Create a new "route" that detects when a user accesses it
    # We'll attach each route to our "app" object
    @app.route("/")
    def home():
        '''Return home page contents'''
        # Query the database
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    app_title = 'Twitoff DS36'

    @app.route('/reset')
    def reset():
        '''Drop existing DB tables and create new ones'''
        # Drop our DB tables
        DB.drop_all()
        # Create tables according to the classes in models.py
        # Like executing an SQL query
        DB.create_all()
        return render_template('base.html', title='Reset DB')

    @app.route('/populate')
    def populate():
        '''Add users and tweets to database'''
        ryan = User(id=1, username='Ryan')
        DB.session.add(ryan)
        julian = User(id=2, username='Julian')
        DB.session.add(julian)
        tweet1 = Tweet(id=1, text="Ryan's tweet", user=ryan)
        DB.session.add(tweet1)
        tweet2 = Tweet(id=2, text="Julian's tweet", user=julian)
        DB.session.add(tweet2)
        DB.session.commit()
        return render_template('base.html', title='Populate')

    # Return our app object after attaching routes to it
    return app

