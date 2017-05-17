from flask import Flask, jsonify, request
import logging
from mongolog.handlers import MongoHandler
import os

app_name = 'bank_microservice'
app = Flask(app_name)
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

logger = logging.getLogger(app_name)
logger.setLevel(logging.DEBUG)
logger.addHandler(MongoHandler.to(host='mongo', port=27017, username=os.environ['MONGODB_USER'], 
									password=os.environ['MONGODB_PASS'], db=os.environ['MONGODB_DATABASE'], 
									collection=os.environ['MONGODB_CAPPEDCOLLECTION_NAME']))


MOCKED_USER_DATA = {
	'Angel': 96543,
	'David': 525,
	'Alf': 6454822,
	'Josue': 5444855,
	'Fred': 6666555,
	'Iron_Man': 99999999
}

@app.route('/balance/<user>', methods=['GET'])
def get_current_position(user):
	log_request_id()
	logger.debug('Requested current balance for user %s' % user)
	if user in MOCKED_USER_DATA:
		logger.info('Current balance for %s is %s' % (user, str(MOCKED_USER_DATA.get(user))))
		return jsonify({'balance': MOCKED_USER_DATA.get(user)}), 200
	else:
		logger.warning('The user %s is not registered in this app' % user)
		return '', 204

@app.route('/balance/<origin_user>/crazy/transaction', methods=['POST'])
def move_crazy_balance(origin_user):
	from random import randint
	log_request_id()
	payload = request.json
	destination_user = payload.get('to', None)
	if origin_user not in MOCKED_USER_DATA:
		logger.error('There is an error with the `origin_user`. It is not registered in this app')
		error = 'The user %s is not registered in this app' % origin_user
		return jsonify({'error': error}), 400
	elif not destination_user or destination_user not in MOCKED_USER_DATA:
		error = 'you must specify destination at `to` attribute and it must be registered'
		logger.error('There is an error with the destination. %s' % error)
		return jsonify({'error': error}), 400
	else:
		crazy_amount = randint(0, 1000)
		logger.info('%s will transfer %s to %s' % (origin_user, str(crazy_amount), destination_user))
		MOCKED_USER_DATA[origin_user] = MOCKED_USER_DATA[origin_user] - crazy_amount
		MOCKED_USER_DATA[destination_user] = MOCKED_USER_DATA[destination_user] + crazy_amount
		logger.info('Thansfer finished')
		return jsonify({'status': 'Transfer finished'}), 201


def log_request_id():
	request_id = request.headers.get('request-id')
	logger.info('The request has id %s' % request_id)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8081, threaded=True)
