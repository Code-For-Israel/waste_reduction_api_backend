from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, Date, String, Float
from flask_migrate import Migrate

db = SQLAlchemy()


class Track(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    #image_data = db.Column(JSON)
    datetime = db.Column(db.DateTime)
    camera_id = db.Column(db.String)
    truck_class = db.Column(db.String)
    probabilities = db.Column(db.Float)
    bbox_x1 = db.Column(db.Float)
    bbox_y1 = db.Column(db.Float)
    bbox_w = db.Column(db.Float)
    bbox_h = db.Column(db.Float)
    

    def __init__(self, detection_time, camera_id, truck_class, probabilities, x1, y1, x2, y2):
        self.datetime = detection_time
        self.camera_id = camera_id
        self.truck_class = truck_class
        self.probabilities = probabilities
        self.bbox_x1 = x1
        self.bbox_y1 = y1
        self.bbox_w = x2
        self.bbox_h = y2