import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from user_CRUD import User_CRUD

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class PostTweet(webapp2.RequestHandler):
    userCrud = User_CRUD()

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        if self.request.get('button') == 'Validate':
            tweet_text = self.request.get('tweet')

            logging.info(tweet_text)

            user = users.get_current_user()

            if user != None:
                # get the user_twitter
                self.userCrud.postTweet(user.user_id(), tweet_text)

            self.redirect("/profile")

