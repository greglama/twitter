import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
import logging

from twitterBaseHandler import TwitterBaseHandler

from crud.user_CRUD import updateUser
from crud.tweets_CRUD import getTweetById, updateTweet

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class EditTweet(TwitterBaseHandler):
    def get(self):
        self.redirectIfNotConnected()
        logout_url = self.getLogoutUrl()

        user_twitter = self.getCurrentTwitterUser()

        tweet_id = self.request.get('tweetID')
        tweet = getTweetById(tweet_id)

        template_values = {
            "userName": user_twitter.name,
            "userPseudo": user_twitter.pseudo,
            "tweet":tweet.text,
            "tweet_id": tweet_id,
            "logout_url": logout_url
        }

        self.sendHTMLresponse(template_values, EditTweet.TEMPLATE_TO_RENDER)

    def post(self):
        self.redirectIfNotConnected()

        #update the content of the tweet
        if self.request.get('button') == 'validate':

            tweetContent = self.request.get('tweet')
            tweet_id = self.request.get('tweet_id')

            updateTweet(tweet_id, tweetContent)
            self.redirect("/profile")
