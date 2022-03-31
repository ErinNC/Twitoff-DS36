''''''
import tweepy
import spacy
from os import getenv
from .models import DB, Tweet, User


# Get our API keys
key = getenv('TWITTER_API_KEY')
secret = getenv('TWITTER_API_KEY_SECRET')

# Authenticate with Twitter
TWITTER_AUTH = tweepy.OAuthHandler(key, secret)

# Open a connection to the API
TWITTER = tweepy.API(TWITTER_AUTH)

def add_or_update_user(username):
    '''Gets twitter user and tweets from twitter DB.
    Gets user with "username" parameter'''
    try:
        # Get the user object from twitter
        twitter_user = TWITTER.get_user(screen_name=username)

        # Check to see if this user is already in the database
        # If they're already in the DB, do nothing
        # If they're not in the DB, insert them
        db_user = (User.query.get(twitter_user.id) or
                User(id=twitter_user.id, username=username))

        # This if statement is equivalent to the above expression
        # if User.query.get(twitter_user.id):
        #     db_user = User.query.get(twitter_user.id)
        # else:
        #     db_user = User(id=twitter_user.id, username=username)

        DB.session.add(db_user)

        # Get the user's tweets from their "timeline"
        tweets = twitter_user.timeline(count=200,
                                    exclude_replies=True,
                                    include_rts=False,
                                    tweet_mode='extended',
                                    since_id=db_user.newest_tweet_id)
        
        # Assign newest_tweet_id
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        # add the individual tweets to the DB
        for tweet in tweets:
            # turns each tweet (object) into a word embedding
            tweet_vector = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(id=tweet.id,
                             text=tweet.full_text[:300],
                             user_id=db_user.id,
                             vect=tweet_vector)
            DB.session.add(db_tweet)


    # Final step to save the DB- only if we successfully add user or tweets
    # Throw an error if add_or_update_user is not successful
    except Exception as error:
        print(f'Error when processing {username}: {error}')
        raise error
    # Otherwise, save user/tweets to the database
    else:
        DB.session.commit()

# Load our pretrained SpaCy Word Embeddings model
nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    '''Turn tweet text into word embeddings'''
    return nlp(tweet_text).vector
