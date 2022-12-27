from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Track(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    #image_data = db.Column(JSON)
    datetime = db.Column(db.DateTime)
    camera_id = db.Column(db.String)
    image_serial = db.Column(db.String)
    camera_name = db.Column(db.String)
    camera_name_he = db.Column(db.String)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    truck_class = db.Column(db.String)
    probability = db.Column(db.Float, nullable=True)
    bbox_cx_fractional = db.Column(db.Float, nullable=True)
    bbox_cy_fractional = db.Column(db.Float, nullable=True)
    bbox_w_fractional = db.Column(db.Float, nullable=True)
    bbox_h_fractional = db.Column(db.Float, nullable=True)
    s3_uri = db.Column(db.String)

    def __init__(self, detection_time, camera_id, camera_name, camera_name_he, latitude, longitude, image_serial, s3_uri, truck_class = None, probability = None, bbox_c_fractional = [None, None, None, None]):
        self.datetime = detection_time
        self.camera_id = camera_id
        self.image_serial = image_serial
        self.camera_name = camera_name
        self.camera_name_he = camera_name_he
        self.latitude = latitude
        self.longitude = longitude
        self.truck_class = truck_class
        self.probability = probability
        self.bbox_cx_fractional = bbox_c_fractional[0]
        self.bbox_cy_fractional = bbox_c_fractional[1]
        self.bbox_w_fractional = bbox_c_fractional[2]
        self.bbox_h_fractional = bbox_c_fractional[3]
        self.s3_uri = s3_uri