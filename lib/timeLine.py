import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.tweets_CRUD import getTimeLineForUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class TimeLine(TwitterBaseHandler):
    def get(self):
        self.redirectIfNotConnected()
        logout_url = self.getLogoutUrl()

        user_twitter = self.getCurrentTwitterUser()
        user_twitter_id = user_twitter.key.id() # id of current user

        tweets = getTimeLineForUser(user_twitter_id) # tweets to put in the timeline

        template_values = {
            "userName": user_twitter.name,
            "userPseudo": user_twitter.pseudo,
            "logout_url": logout_url,
            "list_tweet" : tweets
        }

        self.sendHTMLresponse(template_values, '/template/timeLine.html')
