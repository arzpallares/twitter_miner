# -*- coding: utf-8 -*-
# Base imports
import typing
from dataclasses import dataclass
from abc import ABC, abstractmethod


class TwitterObj(ABC):
    """Abstract Object for common Twitter Object Functions"""
    @abstractmethod
    def generate_dict(self) -> typing.Dict:
        pass


@dataclass
class User(TwitterObj):
    """Object representing a Twitter Account"""
    id: int
    name: str
    url: str
    location: str
    total_followers: int
    total_friends: int
    total_posts: int
    tweets: typing.Optional[typing.List] = None

    def set_posts(self, tweets:typing.List=[]) -> None:
        """Set User's tweets"""
        self.tweets = tweets

    def generate_dict(self) -> typing.Dict:
        """Convert User data into a dictionary"""

        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'location': self.location,
            'total_followers': self.total_followers,
            'total_friends': self.total_friends,
            'total_posts': self.total_posts,
            'tweets': self.tweets,
        }


@dataclass
class Tweet(TwitterObj):
    """Object representing a Tweet"""
    id: str
    user_name: str
    created_at: str
    content: str
    source: str
    retweet_count: int
    favorite_count: int
    coordinates: typing.Dict
    entities: typing.Dict

    def generate_dict(self) -> typing.Dict:
        """Convert Tweet data into a dictionary"""

        return {
            'id': self.id,
            'username': self.user_name,
            'created_at': self.created_at,
            'content': self.content,
            'source': self.source,
            'retweet_count': self.retweet_count,
            'favorite_count': self.favorite_count,
            'coordinates': self.coordinates if self.coordinates else {},
            'entities': self.entities if self.entities else {},
        }