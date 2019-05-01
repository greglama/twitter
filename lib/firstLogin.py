import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from crud.user_CRUD import User_CRUD

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class FirstLogin(webapp2.RequestHandler):

    userCrud = User_CRUD()

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            self.redirect("/")

        else:
            url_logout = users.create_logout_url(self.request.uri)
            template_values = {"logout":url_logout}
            template = JINJA_ENVIRONMENT.get_template('/template/login.html')
            self.response.write(template.render(template_values))

    # add a user in the data store and redirect him toward his profile
    def post(self):
        if self.request.get('button') == 'validate':
            
            name = self.request.get('name').strip()
            pseudo = self.request.get('pseudo').strip()

            user = users.get_current_user()
            if user == None:
                self.redirect("/")
            
            else:
                #TODO check arguments for preExistance
                self.userCrud.createUser(user.user_id(), name, pseudo)
                self.redirect("/profile")
        else:
            self.redirect("/firstLogin")