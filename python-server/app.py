from flask import Flask, render_template
from flask_socketio import emit, SocketIO
from pymongo import MongoClient, CursorType
# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Socket.io
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connected')
def handle_json(json):
    print('received json: ' + str(json))
    from threading import Thread
    thread1 = Thread(target=emit_db_events)
    thread1.start()


def get_cursor(collection):
    print 'getting cursor'
    return collection.find({}, cursor_type=CursorType.TAILABLE_AWAIT)


def emit_db_events():
    # Mongo
    mongo_connection = MongoClient(host='127.0.0.1', port=27017)
    db = mongo_connection.get_database('admin')
    db.authenticate(name='admin', password='admin123')
    collection = db.get_collection('streaming')
    from bson.json_util import dumps
    print 'starting!!!'
    import time
    while True:
        cur = get_cursor(collection)
        while cur.alive:
            for message in cur:
                print(message)
                socketio.emit('log', {'hi': 'mama'}, callback=received())
            time.sleep(0.1)


def received():
    print('received in front')

if __name__ == '__main__':
    socketio.run(app)
