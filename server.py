import tweepy
import os
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
callback = 'https://twitter-blocklist-auth.glitch.me/callback'

@app.route('/auth')
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
    return redirect(url)
  
@app.route('/callback')
def twitter_callback():
    request_token = session['request_token']
    del session['request_token']

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get('oauth_verifier')
    auth.get_access_token(verifier)
    session['token'] = (auth.access_token, auth.access_token_secret)

    return "<ulACCESS_TOKEN:{}\nACCESS_TOKEN_SECRET:{}".format(auth.access_token, auth.access_token_secret)

if __name__ == "__main__":
  app.run(debug=False)
