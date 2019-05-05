import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

import logging
from crud.user_CRUD import getUser

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class TwitterBaseHandler(webapp2.RequestHandler):

    TEMPLATE_TO_RENDER = ""

    @classmethod
    def set_template_to_render(cls, template_to_render):
        cls.TEMPLATE_TO_RENDER = template_to_render

    def getLogoutUrl(self):
        """return a logout url"""
        return users.create_logout_url("/")


    def logUserOut(self):
        """log a user out imediatly"""
        self.redirect(self.getLogoutUrl())
    

    def redirectTowardEmailLogin(self):
        """redirect the user toward the email login page"""
        self.redirect(users.create_login_url(self.request.uri), True, True)


    def redirectIfNotConnected(self):
        """redirect toward email login if the user isn't connected"""
        if self.getCurrentGoogleUser() == None:
            self.redirectTowardEmailLogin()


    def getCurrentGoogleUser(self):
        """return the google user, return None if no user"""
        return users.get_current_user()
    

    def getCurrentTwitterUser(self):
        """return the twitter user (which is built upon the google user),
        return None if no user"""

        #get the google user
        user = self.getCurrentGoogleUser()
        user_twitter = None

        if user != None:
            # get the user twitter
            user_twitter = getUser(user.user_id())

        return user_twitter


    def sendHTMLresponse(self, template_values, templatePath):
        """send the html template to the client with the rendered parameters"""
        
        self.response.headers['Content-Type'] = 'text/html'
        template = JINJA_ENVIRONMENT.get_template(templatePath)
        self.response.write(template.render(template_values))