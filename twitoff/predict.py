import numpy as np
from .models import User
from .twitter import vectorize_tweet
from sklearn.linear_model import LogisticRegression


def predict_user(user0_username, user1_username, hypo_tweet_text):

    # Query for the two users in DB
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()

    # Get the word embeddings from the user's tweets
    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    # Combine their vectorizations into a big X matrix
    X = np.vstack([user0_vects, user1_vects])

    # Create a y vector of 0's and 1's, respectively for each user's tweet
    y = np.concatenate([np.zeros(len(user0.tweets)),
                        np.ones(len(user1.tweets))])

    # Instantiate and train our logistic regression
    log_reg = LogisticRegression()
    log_reg.fit(X,y)

    # Create 2D vectorization (word embedding) of hypothetical tweet
    hypo_tweet_vect = np.array([vectorize_tweet(hypo_tweet_text)])

    # Generate a prediction
    prediction = log_reg.predict(hypo_tweet_vect)

    return prediction[0]
