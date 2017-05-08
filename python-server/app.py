from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socket_io = SocketIO(app)
thread = None


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
    from pymongo import MongoClient, CursorType
    connection = MongoClient(host='127.0.0.1', port=27017)
    db = connection.get_database('admin')
    db.authenticate(name='admin', password='admin123')
    collection = db.get_collection('streaming')
    while True:
        cursor = collection.find({}, cursor_type=CursorType.TAILABLE_AWAIT)
        while cursor.alive:
            for message in cursor:
                message.pop('_id', None)
                socket_io.emit('log', message)

if __name__ == '__main__':
    socket_io.run(app)
