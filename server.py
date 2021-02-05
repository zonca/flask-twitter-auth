import tweepy
import requests
import twitter
import os
from flask import Flask, render_template, request, session, redirect, Response

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]

consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
callback = "https://twitter-blocklist-auth.glitch.me/callback"
signin_with_twitter_button_image = "https://cdn.glitch.com/078e5e4b-c232-486d-b18c-08211207cdf7%2Fsign-in-with-twitter-gray.png.img.fullhd.medium.png?v=1603227771259"


@app.route("/")
def home():
    return '<h1>Authenticate to twitter_blocklist</h1><p><a href="/auth"><img src={} alt="Signin with Twitter"/></a></p>'.format(
        signin_with_twitter_button_image
    )


@app.route("/auth")
def auth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    url = auth.get_authorization_url()
    session["request_token"] = auth.request_token
    return redirect(url)


def authenticate(auth_dict):
    return twitter.Api(**auth_dict, sleep_on_rate_limit=True)


@app.route("/import_blocks", methods=["GET", "POST"])
def import_blocks():
    block = api.CreateBlock  # if not unblock else api.DestroyBlock
    lines = requests.get(request.form["csv_url"]).text.split("\n")
    user_ids = [l.split(",")[0].strip() for l in lines if len(l.strip()) > 0]
    for user_id in user_ids:
        block(user_id=int(user_id))
    return """<h1>twitter_blocklist</h1>

<h2>Import blocks</h2>
<p>Imported {num} blocks into your account</p>
""".format(
        num=len(user_ids)
    )


@app.route("/callback")
def twitter_callback():
    request_token = session["request_token"]
    del session["request_token"]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback)
    auth.request_token = request_token
    verifier = request.args.get("oauth_verifier")
    auth.get_access_token(verifier)
    session["token"] = (auth.access_token, auth.access_token_secret)
    api = authenticate(
        dict(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token_key=auth.access_token,
            access_token_secret=auth.access_token_secret,
        )
    )
    user = api.VerifyCredentials()
    return """<h1>twitter_blocklist</h1>
<p>You are autenticated as {username}</p>

<h2>Import blocks</h2>
<form method="post" action="/import_blocks">
  <label for="csv_url">URL of the CSV file with the blocks (include https://):</label><br>
  <input type="text" id="csv_url" name="csv_url" size=100><br>
</form>
""".format(
        username=user.name
    )


def download_blocks_csv():
    def generate():
        for user in api.GetBlocks():
            yield '{},"{}"\n'.format(user.id_str, user.screen_name)

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=blocks.csv"},
    )


if __name__ == "__main__":
    app.run(debug=False)
