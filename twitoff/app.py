'''Twitoff app made in Flask'''
from flask import Flask, render_template, request
from .twitter import add_or_update_user
from .models import DB, User, Tweet
from .predict import predict_user
from os import getenv


def create_app():
    '''The main app function for twitoff.
    Brings everything together.'''

    # Initialize our app
    app  = Flask(__name__)

    # Database configuration- tells our app where to find DB
    # "registering" our database with the app
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    app_title = 'Twitoff DS36'

    # Create a new "route" that detects when a user accesses it
    # We'll attach each route to our "app" object
    @app.route("/")
    def home():
        '''Return home page contents'''
        # Query the database for all users
        users = User.query.all()
        return render_template('base.html',
                                title='Home',
                                users=users)

    @app.route('/reset')
    def reset():
        '''Drop existing DB tables and create new ones'''
        # Drop our DB tables
        DB.drop_all()
        # Create tables according to the classes in models.py
        # Like executing an SQL query
        DB.create_all()
        return render_template('base.html',
                                title='Reset Database')

    @app.route('/update')
    def update():
        '''Updates all users'''
        usernames = [user.username for user in User.query.all()]
        for username in usernames:
            add_or_update_user(username)
        return render_template('base.html',
                                title='Update Users')
    # Response to submitting a user
    @app.route('/user', methods=['POST'])
    # Response to visiting /user/username
    @app.route('/user/<username>', methods=['GET'])
    def user(username=None, message=''):
        '''Either take the name passed in or pull it from our request.values
        which would be accessed through the user submission'''
        if request.method == 'GET':
            tweets = User.query.filter(User.username==username).one().tweets

        if request.method == 'POST':
            tweets = []
            try:
                username = request.values['user_name']
                add_or_update_user(username)
                message = f'User {username} was successfully added!'
            except Exception as e:
                message = f'Error adding {username}: {e}'
        return render_template('user.html',
                                title=username,
                                tweets=tweets,
                                message=message)
                
    @app.route('/compare', methods= ['POST'])
    def compare():
        user0 = request.values['user0']
        user1 = request.values['user1']

        if user0 == user1:
            message = "Cannot compare a user to themselves"
        else:
            text = request.values['tweet_text']
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = '{} is more likely to be said by {} than {}!'.format(
                text,
                user1 if prediction else user0,
                
            user0 if prediction else user1)
        return render_template('prediction.html',
                                title = 'Prediction',
                                message = message)

    # Return our app object after attaching routes to it
    return app
