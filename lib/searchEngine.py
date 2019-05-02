import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler
from crud.models.tweet import Tweet

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class SearchEngine(TwitterBaseHandler):
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        if self.request.get('button') == 'Go':

            logout_url = self.getLogoutUrl()
            user_twitter = self.getCurrentUserOrRedirect()

            searchText = self.request.get('word')

            # query the tweets that match the search
            # TODO refactorize in a class to perform the search
            tokenizedText = self.userCrud.formatTextForSearch(searchText)
            resultTweets = Tweet.query(Tweet.wordSearch.IN(tokenizedText)).order(-Tweet.dateTime).fetch()

            resultUsers = self.userCrud.searchUserByString(searchText)

            template_values = {
                "userName": user_twitter.name,
                "userPseudo": user_twitter.pseudo,
                "logout_url": logout_url,
                "resultUsers" : resultUsers,
                "resultTweets": resultTweets
            }

            template = JINJA_ENVIRONMENT.get_template('/template/searchResult.html')
            self.response.write(template.render(template_values))