"""Cat URL mangler."""

import sqlalchemy
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, send_from_directory, session, jsonify, Response

from model import Url, connect_to_db, db

import json
import requests
import random
import re
import os
import redis


app = Flask(__name__)

app.secret_key = os.environ["FLASK_SECRET_KEY"]

# Raise an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/cat_path', methods=['POST'])
def cat_path():
    """Encode user original url to cat-url."""

    original_url = request.form.get('original_url')

    if not is_valid_url(original_url):
        return "Please submit a valid url."

    with open('seed.txt', 'r') as f:
        # create a list of cat words
        cat_words = f.readlines()

    need_new_url = True

    while need_new_url:
        
        # initiate randomizer for punctuation
        punctuation = random.randint(0,1)  #  separated by . or -

        cat_path = ''

        for i in range(5):
            word = random.choice(cat_words).strip()  # random cat word
            should_upper = random.randint(0,1) # initiate randomizer for upper / lower case
            word = word.upper() if should_upper else word.lower()
            word = word + ('.' if punctuation else '-')
            cat_path += word

        cat_path = cat_path[:-1]

        # check if url already in db
        if Url.query.filter(Url.cat_path == cat_path).first() is None:
            need_new_url = False

    new_url = Url(original_url=original_url,
                  cat_path=cat_path
                  )

    db.session.add(new_url)
    db.session.commit()

    return cat_path


def is_valid_url(url):
    """Helper function to validate if user entered a valid url."""

    # http://stackoverflow.com/a/7995979
    regex = re.compile(
        r'^(?:https?://)?'  # http:// or https://  make optional
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return url is not None and regex.search(url)


@app.route('/favicon.ico')
def favicon():
    """Cat paw favicon!"""

    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon-paw.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/<user_path>')
def redirect_url(user_path):
    """For a user who enters encoded cat url in a browser, redirect to the original url."""

    # import pdb; pdb.set_trace()
        # increment view counter in redis for url

    # check redis first for key:value, then check db if not there
    destination = redis_connection.get(user_path)

    # create variable cat_path views
    cat_path_views = user_path + "_views"

    if destination:

        # increment cat_path_views and redirect from redis
        redis_connection.incr(cat_path_views)
        return redirect(destination, code=302)

    # if cat_path not in redis, search database
    url = Url.query.filter(Url.cat_path == user_path).first()

    if url is None:
        should_redirect = False
        message = "URL not found."
        if app.debug == True:
            return render_template('error.html',
                                message=message)
        else:
            return redirect('/error')
    else:
        original = url.original_url
        if (original[:7] == "http://") | (original[:8] == "https://"): 
            destination = original
        else:
            destination =  "//" + original

        # add key:value (cat_path: destination) to redis, and time to live expiration (in sec)
        redis_connection.setex(url.cat_path, destination, 60*60)
 
        # increment cat_path_views
        redis_connection.incr(cat_path_views, amount=1)

        return redirect(destination, code=302)


@app.route("/error")
def error():
    raise Exception("Error!")


if __name__ == "__main__":
    connect_to_db(app, os.environ.get("DATABASE_URL"))

    redis_uri = os.environ.get("REDIS_URL") or 'redis://localhost:6379'
    redis_connection = redis.from_url(redis_uri)
    
    # db.create_all()

    PORT = int(os.environ.get("PORT", 5000))
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)

