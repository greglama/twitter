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

class EditProfile(TwitterBaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        logout_url = self.getLogoutUrl()

        user_twitter = self.getCurrentUserOrRedirect()

        template_values = {
            "userName": user_twitter.name,
            "userPseudo": user_twitter.pseudo,
            "logout_url": logout_url
        }
        template = JINJA_ENVIRONMENT.get_template('/template/editProfile.html')
        self.response.write(template.render(template_values))

    def post(self):
        if self.request.get('button') == 'validate':
            name = self.request.get('name').strip()
            
            user = self.getCurrentUserOrRedirect()

            #TODO call CRUD here instead
            user.name = name
            user.put()
            self.redirect("/profile")
