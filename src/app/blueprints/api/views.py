from app.models import Track
from app.models import db
from app.mqtt import convert_to_mqtt_data
from app.mqtt import publish_data_to_mqtt_server
from flask import request, jsonify, Blueprint
import logging
import json
import re
from datetime import datetime

logger = logging.getLogger(__name__)

# define "api" blueprint
api = Blueprint('api', __name__)


# healt-hcheck
@api.route('/validate')
def validate():
    return "All good!"


# method for getting info from the inference server
@api.route('/', methods=['POST'])
def event():
    details = request.get_json()
    details_dict = json.loads(details)
    print(type(details_dict))
    print(f"\n\nStart parsing data\n\n")
    mqtt_data = list()
    for detection_details in details_dict['object_detection_data']:
        parsed_data = ParsingData(detection_details)
        cam, bbox_data, time, s3 = parsed_data.parsing_data_for_db()
        print("\nData pushed to db perfectly \n")
        id_number = parsed_data.push_data_to_db()
        if bbox_data is not None:
            for idx, detection in enumerate(bbox_data):
                mqtt_dict = convert_to_mqtt_data(cam, id_number - len(bbox_data) + idx + 1, detection, time, s3)
                if mqtt_dict is not None:
                    mqtt_data.append(mqtt_dict)
    publish_data_to_mqtt_server(mqtt_data=mqtt_data)
    print("\nData was published to mqtt server perfectly \n")

    return jsonify(details_dict)


class ParsingData:
    
    def __init__(self, detection_details):
        self.detection_details = detection_details
        self.detection_time = str
        self.camera_id = str
        self.camera_name = str
        self.image_serial = str
        self.s3_uri = str 
        self.bbox_details = None


   #Parsing data from Json to db format
    def parsing_data_for_db(self):
        self.axtract_name_date_time()
        self.axtract_detection_data()
        self.camera_name = self.detection_details['camera_name']
        self.s3_uri = self.detection_details['s3_uri']
        print(self.s3_uri, self.camera_id, self.image_serial, self.detection_time, self.bbox_details)
        return self.camera_name, self.bbox_details, self.detection_time, self.s3_uri


    def axtract_name_date_time(self):
        splited_data = self.detection_details['image_id'].split('T')
        camera_id_date, time_data = splited_data[0], splited_data[1]
        self.camera_id = camera_id_date[3:7] # extracting image_serial
        self.image_serial = camera_id_date[7:camera_id_date.index("_")] # extracting camera id
        match_str = re.search(r'\d{2}_\d{2}_\d{4}', camera_id_date)
        match_str = match_str.group() + " " + time_data
        self.detection_time = datetime.strptime(match_str, "%d_%m_%Y %H_%M_%S") # extracting datetime object
        print("\nCamera id, image serial, detection time passed perfectly \n")
        
        
    def axtract_detection_data(self):# DOTO: parse the detection data currently
        bbox_details = self.detection_details["detection_results"]
        if type(bbox_details) == str:
            print('There are no detections')
        else:
            self.bbox_details = list(zip(bbox_details['classes'], bbox_details['probabilities'], bbox_details['bboxs_cx_cy_w_h_fractional']))
            print("\nDetection list passed perfectly \n")
    
    #Push data to db
    def push_data_to_db(self):
        if self.bbox_details is None:
            track = Track(self.detection_time, self.camera_id, self.camera_name, self.image_serial, self.s3_uri)
            db.session.add(track) 
            db.session.commit()
        else:
            for bbox_details in self.bbox_details:
                track = Track(self.detection_time, self.camera_id, self.camera_name, self.image_serial, self.s3_uri, *list(bbox_details))
                db.session.add(track) 
                db.session.commit()

        db.session.refresh(track)
        return track.id
        
                
                
                
                
                
                
                
                
                
                
                
                
                
    #Parsing data from Json to db format
# def parsing_data_for_db(details):
#     details = json.loads(details)
#     detection_time, camera_id, image_serial = axtract_name_date_time(details['image_id'])
#     detections_list = axtract_detection_data(details['detections_result'])
#     s3_uri = details['s3_uri']
#     return  detection_time, camera_id, image_serial, s3_uri, detections_list
   
#     #Axtracting camera id, detection date time
# def axtract_name_date_time(image_data: str):
#     splited_data = image_data.split('T')
#     camera_id_date, time_data = splited_data[0], splited_data[1]
#     camera_id = camera_id_date[7:camera_id_date.index("_")] #axtracting camera id
#     image_serial = camera_id_date[3:7] #axtracting image_serial
#     match_str = re.search(r'\d{2}_\d{2}_\d{4}', camera_id_date)
#     match_str = match_str.group() +" "+ time_data
#     detection_time = datetime.strptime(match_str, "%d_%m_%Y %H_%M_%S")#axtracting datetime object
#     return detection_time, camera_id, image_serial

    #Axtracting detection data - class, probabilities, bbox
# def axtract_detection_data(detections):
#     detection_list = []
#     for i in range(len(detections['classes'])):
#         detection_list.append([detections['classes'][i], detections['probabilities'][i], *detections['bbox_cx_cy_w_h_fractional'][i]])
#     return detection_list

# def push_data_to_db(detection_time, camera_id, image_serial, s3_uri, truck_class, probabilities, x1, y1, x2, y2):
#     track = Track(detection_time, camera_id, image_serial, s3_uri, truck_class, probabilities, x1, y1, x2, y2)
#     db.session.add(track)
#     db.session.commit()
    