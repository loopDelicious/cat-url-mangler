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

app = Flask(__name__)

app.secret_key = os.environ["FLASK_SECRET_KEY"]

# Raise an error if you use an undefined variable in Jinja2
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/encode_url', methods=['POST'])
def encode_url():
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

        encode_url = ''

        for i in range(5):
            word = random.choice(cat_words).strip()  # random cat word
            should_upper = random.randint(0,1) # initiate randomizer for upper / lower case
            word = word.upper() if should_upper else word.lower()
            word = word + ('.' if punctuation else '-')
            encode_url += word

        encode_url = encode_url[:-1]

        # check if url already in db
        if Url.query.filter(Url.encode_url == encode_url).first() is None:
            need_new_url = False

    new_url = Url(original_url=original_url,
                  encode_url=encode_url
                  )

    db.session.add(new_url)
    db.session.commit()

    return encode_url


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


@app.route('/<path>')
def redirect_url(path):
    """For a user who enters encoded url in a browser, redirect to the original url."""

    # import pdb; pdb.set_trace()
    should_redirect = True

    while should_redirect:
        url = Url.query.filter(Url.encode_url == path).first()
        # check if url in db
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
            return redirect(destination, code=301)

@app.route("/error")
def error():
    raise Exception("Error!")


if __name__ == "__main__":
    # if os.environ.get("NO_DEBUG"):
        # app.debug == False
    connect_to_db(app, os.environ.get("DATABASE_URL"))
    # app.run()
    db.create_all()

    PORT = int(os.environ.get("PORT", 5000))
    # app.run(host="0.0.0.0", port=PORT)

    DEBUG = "NO_DEBUG" not in os.environ
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)

