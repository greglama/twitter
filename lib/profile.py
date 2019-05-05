import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.tweets_CRUD import getAllTweetsOfUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Profile(TwitterBaseHandler):
    def get(self):
        self.redirectIfNotConnected()
        logout_url = self.getLogoutUrl()

        user_twitter = self.getCurrentTwitterUser()
        user_twitter_id = user_twitter.key.id()
        
        # get the tweets of the user
        tweets = getAllTweetsOfUser(user_twitter_id)

        template_values = {
            "userName": user_twitter.name,
            "userPseudo": user_twitter.pseudo,
            "description": user_twitter.description,
            "logout_url": logout_url,
            "list_tweet" : tweets
        }

        self.sendHTMLresponse(template_values, '/template/userProfile.html')