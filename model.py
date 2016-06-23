"""Models and database functions for catURL project."""

from flask_sqlalchemy import SQLAlchemy

# Connection to the PostgreSQL database through the Flask-SQLAlchemy library.
# On this, we can find the `session` object, where we do most of our interactions.

db = SQLAlchemy()

##############################################################################
# Model definitions

class URL(db.Model):
    """URLs that are uploaded by users."""

    __tablename__ = "urls"

    url_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    original_url = db.Column(db.String(1000), nullable=False)
    encode_url = db.Column(db.String(1000), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed, for human readability."""

        return "<Url url_id=%s original_url=%s encode_url=%s>" % (self.url_id, 
            self.original_url, self.encode_url)

# class User(db.Model):
#     """User of walking website."""

#     __tablename__ = "users"

#     user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     email = db.Column(db.String(70), nullable=False)
#     password_hash = db.Column(db.String(80), nullable=False)
#     salt = db.Column(db.String(40), nullable=False)

#     def __repr__(self):
#         """Provide helpful representation when printed, for human readability."""

#         return "<User user_id=%s email=%s>" % (self.user_id, self.email)
           
#     def __init__(self, email, password):
#         """Instantiate a user object within the User class with salted passwords."""

#         self.email = email
#         self.salt = bcrypt.gensalt()
#         self.password_hash = bcrypt.hashpw(password.encode('utf8'), self.salt.encode('utf8'))

#     def verify_password(self, password):
#         """Verify user's password, a method that can be called on a user."""

#         password_hash = bcrypt.hashpw(password.encode('utf8'), self.salt.encode('utf8'))

#         if self.password_hash == password_hash:
#             return True
#         else:
#             return False

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
    print "Connected to DB."