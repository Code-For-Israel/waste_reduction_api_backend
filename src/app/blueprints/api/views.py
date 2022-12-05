from app.models import Track
from app.models import db
from flask import request, jsonify, Blueprint
import logging

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
    print("*********************************\n")
    print(type(details))
    print("*********************************\n")

    track = Track(details)
    db.session.add(track)
    db.session.commit()

    return jsonify(details)
