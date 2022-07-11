# Twitoff Post Predictor
Develop a prototype full-stack web application backed by Data Science using Python, Flask, and SQLAlchemy.

## Purpose of the App
The Twitoff Post Predictor app allows the user to select Twitter accounts, accepts a user-input message, and predicts which of two users most likely shared this tweet based off of their tweet history (obtained from the Twitter API).

## What the User Does
- Enter two (or more) twitter usernames.
- Select the usernames of the accounts that they would like to compare
- Enter some text that they would like to make a prediction with. 
- Click the "Compare Users" button to generate a prediction.

## What the App Does
- Takes the provided usernames and uses them to query the Twitter API for the users' most recent tweets.
- Save the users and tweets from the Twitter API to our database
- Use SpaCy to turn the text of our tweets into a numeric representation called "word embeddings"
- Pass those word embeddings into a logistic regression to predict which user is more likely to have said that tweet.
- Return the prediction to the user and display it on the frontend.

## Installed Packages/Libraries
- flask
- jinja2
- flask-sqlalchemy
- tweepy
- spacy
- python-dotenv
- scikit-learn
