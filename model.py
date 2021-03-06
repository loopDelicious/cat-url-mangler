"""Models and database functions for catURL project."""

from flask_sqlalchemy import SQLAlchemy

# Connection to the PostgreSQL database through the Flask-SQLAlchemy library.
# On this, we can find the `session` object, where we do most of our interactions.

db = SQLAlchemy()


##############################################################################
# Model definition

class Url(db.Model):
    """URLs that are uploaded by users."""

    __tablename__ = "urls"

    url_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    original_url = db.Column(db.String(10000), nullable=False)
    cat_path = db.Column(db.String(1000), nullable=False) # path following http://<hostname> or https://<hostname>

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Url url_id=%s original_url=%s cat_path=%s>" % (self.url_id, 
            self.original_url, self.cat_path)


##############################################################################

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///urls'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    db.create_all()
    print "Connected to DB."


