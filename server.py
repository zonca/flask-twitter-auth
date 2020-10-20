import tweepy
import os
from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
callback = "https://twitter-blocklist-auth.glitch.me/callback"
signin_with_twitter_button_image = "https://cdn.glitch.com/078e5e4b-c232-486d-b18c-08211207cdf7%2Fsign-in-with-twitter-gray.png.img.fullhd.medium.png?v=1603227771259"


@app.route("/")
def home():
    return '<h1>Generate access token and secret for twitter_blocklist</h1><a href="/auth"><img src={} alt="Signin with Twitter"/></a>'.format(
        signin_with_twitter_button_image
    )


@app.route("/auth")
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session["request_token"] = auth.request_token
    return redirect(url)


@app.route("/callback")
def twitter_callback():
    request_token = session["request_token"]
    del session["request_token"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get("oauth_verifier")
    auth.get_access_token(verifier)
    session["token"] = (auth.access_token, auth.access_token_secret)

    return "<dl><dt>ACCESS_TOKEN</dt><dd>{}</dd><dt>ACCESS_TOKEN_SECRET</dt><dd>{}</dd></dl>".format(
        auth.access_token, auth.access_token_secret
    )


if __name__ == "__main__":
    app.run(debug=False)
