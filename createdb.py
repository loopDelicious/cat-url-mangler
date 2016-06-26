from model import connect_to_db
from server import app, db

if __name__ == "__main__":
    
    connect_to_db(app)
    db.create_all()