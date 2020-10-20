import tweepy
import os
from flask import Flask, render_template, request

app = Flask(__name__)

consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
callback = 'https://twitter-blocklist-auth.glitch.me/callback'

@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)

if __name__ == "__main__":
  app.run(debug=True)
