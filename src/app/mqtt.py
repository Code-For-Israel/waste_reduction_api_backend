import pendulum
import json
import paho.mqtt.client as mqtt


def convert_to_mqtt_data(cam, id_number, detection, time, s3):
    truck = detection[0]
    probability = int(detection[1] * 100)
    id_number = id_number
    dt = pendulum.instance(time).in_tz('Israel').to_rfc850_string()
    if truck == 'covered':
        mqtt_dict = {"topic": "Playground/ml/" + cam.replace(" ", "") + "/Notifies",
                     "message": {'id': id_number, 'p': probability, 'time': dt, 's3': s3}}
        return mqtt_dict
    return None


def on_publish(client, userdata, mid):
    print("sent a message to MQTT server")


def publish_data_to_mqtt_server(username='', password='', host='', mqtt_data=[{"topic": None, "message": None}]):
    mqttClient = mqtt.Client("truck_detection")
    mqttClient.username_pw_set(username=username, password=password)
    mqttClient.on_publish = on_publish
    mqttClient.connect(host, 1883)
    # start a new thread
    mqttClient.loop_start()

    # Why use msg.encode('utf-8') here
    # MQTT is a binary based protocol where the control elements are binary bytes and not text strings.
    # Topic names, Client ID, Usernames and Passwords are encoded as stream of bytes using UTF-8.
    for data in mqtt_data:
        # topic + message
        topic = data['topic']
        message = data['message']
        print('topic', topic)
        print('message', message)
        msg = json.dumps(message)
        info = mqttClient.publish(
            topic=topic,
            payload=msg.encode('utf-8'),
            qos=0,
        )
        # Because published() is not synchronous,
        # it returns false while he is not aware of delivery that's why calling wait_for_publish() is mandatory.
        info.wait_for_publish()
        print(info.is_published())
        print()

