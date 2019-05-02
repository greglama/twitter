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

class TimeLine(TwitterBaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        logout_url = self.getLogoutUrl()
        
        user_twitter = self.getCurrentUserOrRedirect()

        user_twitter_id = user_twitter.key.id() # id of current user

        tweets = self.userCrud.getTimeLineForUser(user_twitter_id)
        
        template_values = {
            "userName": user_twitter.name,
            "userPseudo": user_twitter.pseudo,
            "logout_url": logout_url,
            "list_tweet" : tweets
        }

        template = JINJA_ENVIRONMENT.get_template('/template/timeLine.html')
        self.response.write(template.render(template_values))
