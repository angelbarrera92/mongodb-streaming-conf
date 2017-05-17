from flask import Flask, request
import random
import logging
import requests
from mongolog.handlers import MongoHandler
import os

app_name = 'crazy_aggregate_app'
app = Flask(app_name)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

logger = logging.getLogger(app_name)
logger.setLevel(logging.DEBUG)
logger.addHandler(MongoHandler.to(host='mongo', port=27017, username=os.environ['MONGODB_USER'], 
									password=os.environ['MONGODB_PASS'], db=os.environ['MONGODB_DATABASE'], 
									collection=os.environ['MONGODB_CAPPEDCOLLECTION_NAME']))

@app.route('/')
def home():
	import socket
	hostname = socket.gethostname()
	logger.debug('I am %s and i am serving the %s app' % (hostname, app_name))
	return 'Hello World, i am %s' % hostname

@app.route('/demo/<user>')
def do_some_crazy_transfers(user):
	log_request_id()
	logger.info('I am going to check balance for user %s' % user)
	response = requests.get('http://bank_microservice:8081/balance/%s' % user, headers=request.headers)
	if response.status_code == 200:
		balance = response.json()['balance']
		if balance > 0:
			logger.info('Yes, i will do some crazy transactions')
			destination = _choose_random_destination()
			logger.info('Choosen destination is: %s' % destination)
			payload = {'to': destination}
			response = requests.post('http://bank_microservice:8081/balance/%s/crazy/transaction' % user, json=payload, headers=request.headers)
			if response.status_code == 201:
				response = requests.get('http://bank_microservice:8081/balance/%s' % user, headers=request.headers)
				new_balance = response.json()['balance']
				logger.info('Ole Ole Ole!. New Balance is %s' % str(new_balance))
				return 'Ole Ole Ole!. New Balance is %s' % str(new_balance)
			else:
				bad_message = response.json()['error']
				logger.warning('Uhmmm something is badddddd :( -> %s' % bad_message)
				return 'Something bad, Try Again'
		else:
			logger.warning('The user %s is poor. We can do nothing but wait' % user)
			return 'The user %s is poor. We can do nothing but wait' % user
	else:
		logger.warning('There is nothing to do here, try again')
		return 'Try Again!'


def _choose_random_destination():
	possible_users = ['Angel', 'David', 'Alf', 'Josue', 'Fred', 'Iron_Man', 'Ramon', 'NoBody', 'Kim']
	return random.choice(possible_users)


def log_request_id():
	request_id = request.headers.get('request-id')
	logger.info('The request has id %s' % request_id)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, threaded=True)
