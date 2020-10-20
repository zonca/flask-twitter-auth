from flask import Flask, render_template, request
import tweepy

app = Flask(__name__)

@app.route('/')
def index():
	
	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	
	search = request.args.get('q')
	
	public_tweets = api.user_timeline(search)

	return render_template('home.html', tweets=public_tweets)

if __name__ == "__main__":
  app.run()
