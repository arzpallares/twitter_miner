# -*- coding: utf-8 -*-
from models import handlers

if __name__ == "__main__":
    """
    This application will:
    1- Get command prompt arguments and save it into variables
    2- Validate Twitter Auth
    3- Get User's data
    4- Save results into  a JSON and YAML files
    """
    # Create argument handler
    arghandler = handlers.ArgHandler()
    args = arghandler.read_args()

    # Create Authorizer
    auth = handlers.Authorizer()
    # Validate if KEYS are valid
    api = auth.auth_user()

    # Create ETL Handler
    handler = handlers.ETLHandler(api)

    # Get User(s)
    user = handler.get_user_data(args.account)

    if user:
        # Run only if Account generated no exceptions
        user_timeline = handler.get_user_timeline(user, 30)

        # List of User's last 20 tweets
        tweets = []

        for status in user_timeline:
            tweet = handler.get_tweet_data(status=status)
            obj = tweet.cast_to_dict()
            tweets.append(obj)
        
        user.set_posts(tweets=tweets)

        handler.convert_to_json(user.cast_to_dict())
        handler.convert_to_yaml(user.cast_to_dict())