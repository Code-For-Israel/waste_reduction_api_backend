from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Date, String, Float

db = SQLAlchemy()

class Track(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(JSON)
    datetime = db.Column(Date)
    camera_id = db.Column(String)
    truck_class = db.Column(String)
    probabilities = db.Column(Float)

    def __init__(self, image_data):
        self.image_id = image_data

