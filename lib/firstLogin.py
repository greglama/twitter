import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.user_CRUD import createUser

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
            # add a user in the data store and redirect him toward his profile
            name = self.request.get('name').strip()
            pseudo = self.request.get('pseudo').strip()
            description = self.request.get('description').strip()
            
            #TODO check if pseudo already exist...
            createUser(user.user_id(), name, pseudo, description)
            self.redirect("/profile")

        else:
            self.redirect("/firstLogin")