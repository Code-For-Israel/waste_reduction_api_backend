from db_setting import db, Track, app
from flask import request, jsonify

db.create_all()
@app.route('/', methods=['POST'])
def event():
    details = request.get_json()
    print("*********************************\n")
    print(type(details))
    print("*********************************\n")

    track = Track(details)
    db.session.add(track)
    db.session.commit()
    
    return jsonify(details)

if __name__ == '__main__':
    app.run(debug=True)