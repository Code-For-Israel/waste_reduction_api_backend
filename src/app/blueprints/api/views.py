from app.models import Track
from app.models import db
from flask import request, jsonify, Blueprint
import logging, json, re
from datetime import datetime

logger = logging.getLogger(__name__)

# define "api" blueprint
api = Blueprint('api', __name__)


# healt-hcheck
@api.route('/validate')
def validate():
    return "All good!"

# method for getting info from the inferenca server
@api.route('/', methods=['POST'])
def event():
    details = request.get_json()
    camera_id, detection_time, detections_list = parsing_data_for_db(details)
    for detection in detections_list:
        push_data_to_db(detection_time, camera_id, *detection)
    return jsonify(details)

    #Parsing data from Json to db format
def parsing_data_for_db(details):
    details = json.loads(details)
    camera_id, detection_time = axtract_name_date_time(details['image_id'])
    detections_list = axtract_detection_data(details['detections_result'])
    return camera_id, detection_time, detections_list
   
    #Axtracting camera id, detection date time
def axtract_name_date_time(image_data: str):
    splited_data = image_data.split('T')
    camera_id_date, time_data = splited_data[0], splited_data[1]
    camera_id = camera_id_date[:camera_id_date.index("_")] #axtracting camera id
    match_str = re.search(r'\d{2}_\d{2}_\d{4}', camera_id_date)
    match_str = match_str.group() +" "+ time_data
    datetime_object = datetime.strptime(match_str, "%d_%m_%Y %H_%M_%S")#axtracting datetime object
    return camera_id, datetime_object

    #Axtracting detection data - class, probabilities, bbox
def axtract_detection_data(detections):
    detection_list = []
    for i in range(len(detections['classes'])):
        detection_list.append([detections['classes'][i], detections['probabilities'][i], *detections['bbox_cx_cy_w_h'][i]])
    return detection_list

    #Push data to db
def push_data_to_db(datetime, camera_id, truck_class, probabilities, x1, y1, x2, y2):
    track = Track(datetime, camera_id, truck_class, probabilities, x1, y1, x2, y2)
    db.session.add(track)
    db.session.commit()