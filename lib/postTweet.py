import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class PostTweet(TwitterBaseHandler):

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        if self.request.get('button') == 'Validate':
            tweet_text = self.request.get('tweet')

            user = self.getCurrentGoogleUserOrRedirect()

            if user != None:
                # post the tweet
                self.userCrud.postTweet(user.user_id(), tweet_text)

            self.redirect("/profile")

