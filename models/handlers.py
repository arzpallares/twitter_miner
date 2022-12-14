# -*- coding: utf-8 -*-
# Base imports
import os
import typing

# Data Format imports
import json
import ruamel.yaml

# Environment imports
from dotenv import load_dotenv

# Tweetpy imports
import tweepy
from tweepy.errors import Unauthorized

# Model import
from . import models

# Load Environment variables
load_dotenv()

# SET UP API VARIABLES
CONSUMER_KEY = os.getenv("CONSUMER_KEY") or ""
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET") or ""
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN") or ""
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET") or ""


class ETLHandler:
    """Handle ETL processes for the Twitter API"""

    def __init__(self, api:tweepy.API) -> None:
        self.api = api

    def get_user_data(self, account:str="elonmusk") -> models.User:
        """Get User account information"""
        try:
            target_user = self.api.get_user(screen_name=account)

            id = target_user.id
            name = target_user.name
            location = target_user.location
            followers = target_user.followers_count
            friends = target_user.friends_count

            user = models.User(
                id=id,
                name=name,
                url=target_user.url,
                location=location,
                total_followers=followers,
                total_friends=friends,
                total_posts=target_user.statuses_count)

            return user
        
        except tweepy.errors.NotFound as err:
            """Build error message and return False"""
            message = f"Error {err.response.status_code}. {err.api_messages[0]}"
            print(message)
            
            return False

    def get_tweet_data(self, status:tweepy.models.Status) -> models.Tweet:
        """Transform Status model into a Tweet object"""
        
        return models.Tweet(
            id=status.id_str,
            user_name=status.user.screen_name,
            created_at=status.created_at.strftime("%b %d, %Y %H:%M:%S %Z%z"),
            content=status.text,
            source=status.source,
            coordinates=status.coordinates,
            retweet_count=status.retweet_count,
            favorite_count=status.favorite_count,
            entities=status.entities,
        )

    def get_user_timeline(self, user:models.User, count:int=20) -> typing.List:
        """Get User Timeline Posts"""
        return self.api.user_timeline(user_id=user.id, count=count)

    def check_data_folder(self, output_folder:str=None):
        """Checks if data folder exists, if not create it"""
        
        self.path = output_folder if output_folder else os.path.join(os.getcwd(), "data")

        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def convert_to_json(self, twitter_dict:typing.Dict, output_name:str="file", output_folder:str=None) -> None:
        """Format tweets data and store it into a JSON file"""
        self.check_data_folder(output_folder=output_folder)
        
        filename = f"{self.path}/{output_name}.json"

        with open(filename, mode="w", encoding='utf-8-sig') as file:
            json.dump(twitter_dict, file, indent=4)

        return file

    def convert_to_yaml(self, twitter_dict:typing.Dict, output_name:str="file", output_folder:str=None) -> None:
        """To be Implemented in API Version"""
        """Format tweets data and store it into a YAML file"""
        self.check_data_folder(output_folder=output_folder)

        filename = f"{self.path}/{output_name}.yaml"

        with open(filename, mode="w", encoding='utf-8-sig') as file:
            yaml = ruamel.yaml.YAML()
            yaml.indent(sequence=4, offset=2)
            yaml.dump(twitter_dict, file)

        return file


class Authorizer:
    """Handle Twitter API authorization"""

    def auth_user(self) -> tweepy.API:
        """Authenticates User and generates api connection"""
        # Creating Authentication Object
        try:
            auth = tweepy.OAuth1UserHandler(
                CONSUMER_KEY,
                CONSUMER_SECRET,
                ACCESS_TOKEN,
                ACCESS_TOKEN_SECRET
            )

            api = tweepy.API(auth)

        except Unauthorized as err:
            raise Unauthorized(err)

        return api