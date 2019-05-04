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

class FirstLogin(TwitterBaseHandler):

    def get(self):
        
        self.redirectIfNotConnected()
        url_logout = self.getLogoutUrl()

        template_values = {"logout":url_logout}
        self.sendHTMLresponse(template_values, '/template/login.html')

    def post(self):        
        self.redirectIfNotConnected()

        #get the current connected user, redirect toward email login if none
        user = self.getCurrentGoogleUser()

        if self.request.get('button') == 'validate':
            name = self.request.get('name').strip()
            pseudo = self.request.get('pseudo').strip()
            description = self.request.get('description').strip()
            
            #TODO check arguments for already existing pseudo...
            # add a user in the data store and redirect him toward his profile
            self.userCrud.createUser(user.user_id(), name, pseudo, description)
            self.redirect("/profile")

        else:
            self.redirect("/firstLogin")