from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO
import os

app = Flask(__name__, static_url_path='')
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
socket_io = SocketIO(app)
thread = None

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)


@app.route('/')
def index():
    return render_template('index.html', async_mode=socket_io.async_mode)


@socket_io.on('connected')
def handle_json(json):
    print('received json: ' + str(json))
    global thread
    if thread is None:
        thread = socket_io.start_background_task(target=mongo_streams)


def mongo_streams():
    from bson import json_util
    from pymongo import MongoClient, CursorType
    import json
    connection = MongoClient(host='mongo', port=27017)
    db = connection.get_database(os.environ['MONGODB_DATABASE'])
    db.authenticate(name=os.environ['MONGODB_USER'], password=os.environ['MONGODB_PASS'])
    collection = db.get_collection(os.environ['MONGODB_CAPPEDCOLLECTION_NAME'])
    while True:
        cursor = collection.find({}, cursor_type=CursorType.TAILABLE_AWAIT)
        while cursor.alive:
            for message in cursor:
                print(json.loads(json_util.dumps(message)))
                socket_io.emit('log', json.loads(json_util.dumps(message)))

if __name__ == '__main__':
    socket_io.run(app, host='0.0.0.0', port=5000)
