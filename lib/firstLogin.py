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
        self.response.headers['Content-Type'] = 'text/html'

        url_logout = self.getLogoutUrl()

        #Will redirect toward login if the user hasn't gone through the email login process
        self.getCurrentGoogleUserOrRedirect()

        template_values = {"logout":url_logout}
        template = JINJA_ENVIRONMENT.get_template('/template/login.html')
        self.response.write(template.render(template_values))

    def post(self):        
        #get the current connected user, redirect toward email login if none
        user = self.getCurrentGoogleUserOrRedirect()

        if self.request.get('button') == 'validate':
            name = self.request.get('name').strip()
            pseudo = self.request.get('pseudo').strip()
            
            #TODO check arguments for already existing pseudo...
            # add a user in the data store and redirect him toward his profile
            self.userCrud.createUser(user.user_id(), name, pseudo)
            self.redirect("/profile")

        else:
            self.redirect("/firstLogin")