import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from crud.user_CRUD import User_CRUD

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class TwitterBaseHandler(webapp2.RequestHandler):
    userCrud = User_CRUD()

    def getLogoutUrl(self):
        """return a logout url"""
        return users.create_logout_url(self.request.uri)
    
    def getCurrentGoogleUserOrRedirect(self):
        """return the current google user, or redirect toward login if it doesn't exist"""
        #get the google user
        user = users.get_current_user()
        
        if user == None:
            self.redirect("/")
        
        return user

    def getCurrentUserOrRedirect(self):
        """return the current user_twitter, or redirect toward login if it doesn't exist"""

        #get the google user
        user = users.get_current_user()

        user_twitter = None

        if user != None:
            # get the user twitter
            user_twitter = self.userCrud.getUser(user.user_id())

        # redirect toward login if no user
        if user_twitter == None:
            self.redirect("/")
        
        return user_twitter