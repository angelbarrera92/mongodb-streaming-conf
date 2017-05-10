from flask import Flask
import logging
from mongolog.handlers import MongoHandler

app = Flask(__name__)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(MongoHandler.to(host='127.0.0.1', port=27017, username='admin', password='admin123', 
									db='admin', collection='streaming'))

@app.route('/')
def home():
	import socket
	hostname = socket.gethostname()
	logger.debug('I am %s and i am serving the hello world app' % hostname)
	return 'Hello World, i am %s' % hostname

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8080, threaded=True)
