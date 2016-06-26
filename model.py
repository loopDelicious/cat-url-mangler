"""Models and database functions for catURL project."""

from flask_sqlalchemy import SQLAlchemy


# Connection to the PostgreSQL database through the Flask-SQLAlchemy library.
# On this, we can find the `session` object, where we do most of our interactions.

db = SQLAlchemy()

##############################################################################
# Model definitions

class Url(db.Model):
    """URLs that are uploaded by users."""

    __tablename__ = "urls"

    url_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    original_url = db.Column(db.String(10000), nullable=False)
    encode_url = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Url url_id=%s original_url=%s encode_url=%s>" % (self.url_id, 
            self.original_url, self.encode_url)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///urls'
    db.app = app
    db.init_app(app)



if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."


