import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.tweets_CRUD import postTweet

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class PostTweet(TwitterBaseHandler):
    def post(self):
        self.redirectIfNotConnected()
        
        if self.request.get('button') == 'Validate':
            tweet_text = self.request.get('tweet')

            user = self.getCurrentGoogleUser()
            postTweet(user.user_id(), tweet_text)

            self.redirect("/profile")

