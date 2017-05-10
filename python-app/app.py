from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
	import socket
	return 'Hello World, i am %s' % socket.gethostname()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, threaded=True)
