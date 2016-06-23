"""Cat mangler."""

import sqlalchemy
from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify, Response

from model import URL, connect_to_db, db

import json
import requests

from datetime import date

app = Flask(__name__)

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

    # encode url

    new_url = Url(original_url=original_url,
                  encode_url=encode_url
                  )

    db.session.add(new_url)
    db.session.commit()



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
    # app.run(host='0.0.0.0')