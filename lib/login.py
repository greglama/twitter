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

class Login(TwitterBaseHandler):
    def get(self):
        self.redirectIfNotConnected()

        # if it is its first connexion
        if self.getCurrentTwitterUser() == None:
            self.redirect("/firstLogin")

        else:
            self.redirect("/profile")
