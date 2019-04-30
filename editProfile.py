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

class EditProfile(webapp2.RequestHandler):
    userCrud = User_CRUD()

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()
        logout_url = users.create_logout_url(self.request.uri)
        user_twitter = None

        if user != None:
            # get the user twitter
            user_twitter = self.userCrud.getUser(user.user_id())

        # redirect toward login if no user
        if user_twitter == None:
            self.redirect("/")

        # fulfill the template otherwise and display the html
        else:

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
            #jinja user
            user = users.get_current_user()
            #twitter user
            user = self.userCrud.getUser(user.user_id())
            user.name = name
            user.put()
            self.redirect("/profile")