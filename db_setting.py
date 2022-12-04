from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, Column, Integer, String, Date, Float
from config import BaseConfig
import os

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
app.config.from_object(BaseConfig)

basedir = os.path.abspath(os.path.dirname(__file__))
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:data1@localhost/track_detection'
#app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


class Track(db.Model):
    __tablename__ = 'events' 
    id = db.Column(db.Integer, primary_key=True)
    image_data = db.Column(JSON)
    datetime = db.Column(Date)
    camera_id = db.Column(String)
    truck_class = db.Column(String)
    probabilities = db.Column(Float)
    
    # Parsing
    # date of pushing into db insertts
    # link to 3b 
    # date time
    # camera id 
    # class
    # probabilities
    # x1,2 
    # y1,2 
   
    def __init__(self, image_data):
        self.image_id = image_data
        
