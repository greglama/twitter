import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.user_CRUD import updateUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class EditProfile(TwitterBaseHandler):
    def get(self):
        self.redirectIfNotConnected()
        logout_url = self.getLogoutUrl()
        
        user_twitter = self.getCurrentTwitterUser()

        template_values = {
            "userName": user_twitter.name,
            "userPseudo": user_twitter.pseudo,
            "description": user_twitter.description,
            "logout_url": logout_url
        }

        self.sendHTMLresponse(template_values, '/template/editProfile.html')

    def post(self):
        self.redirectIfNotConnected()

        #update the name and description of a user
        if self.request.get('button') == 'validate':

            name = self.request.get('name').strip()
            description = self.request.get('description').strip()
            
            user_twitter_id = self.getCurrentTwitterUser().key.id()

            updateUser(user_twitter_id, name, description)
            self.redirect("/profile")
