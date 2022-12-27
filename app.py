# -*- coding: utf-8 -*-
# Fast API
from fastapi import FastAPI

# Data Handlers
from models import handlers

app = FastAPI()

@app.get('/')
async def welcome():
    return {'message': 'Welcome to Twitter Miner'}

@app.get('/account/{account_name}')
async def account(account_name:str = 'elonmusk', format:str = 'json'):
    """Return Twitter Account Data"""
    return main(account_name, format)

def main(account:str, format:str):
    """
    This application will:
    1- Receive a GET request with a Twitter user account
    2- Validate Twitter Auth
    3- Get User's data
    4- Save results into  a JSON and YAML files
    """

    # Create Authorizer
    auth = handlers.Authorizer()
    # Validate if KEYS are valid
    api = auth.auth_user()

    # Create ETL Handler
    handler = handlers.ETLHandler(api)

    # Get User(s)
    user = handler.get_user_data(account)

    if user:
        # Run only if Account generated no exceptions
        user_timeline = handler.get_user_timeline(user, 30)

        # List of User's last 20 tweets
        tweets = []

        for status in user_timeline:
            tweet = handler.get_tweet_data(status=status)
            obj = tweet.generate_dict()
            tweets.append(obj)
        
        user.set_posts(tweets=tweets)

        if format == 'json':
            return {'result': user.generate_dict()}
        else:
            return {'Message': 'Invalid file format. Available formats are JSON & YAML.'}