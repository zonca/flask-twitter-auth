# Twitter app authentication

Flask application to authenticate a Twitter use using
the 3 legged oauth and print back the Access Token
and the Access Token Secret.

## How to set it up

- Fork the project on Glitch <https://glitch.com/~twitter-blocklist-auth>
- Create a Twitter app with permissions to authenticate as other users
- Copy the `TWITTER_CONSUMER_KEY` and `TWITTER_CONSUMER_SECRET` to the Glitch `.env`
- Generate a unique key (for example with a password generator) `SECRET_KEY` and add to `.env`
- Modify the `callback` URL in `server.py`
