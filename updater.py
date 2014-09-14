import requests
import time

WAIT_TIME = 1800
while True:
	requests.get('http://127.0.0.1:5000/force_populate_database_secret_key')
	time.sleep(WAIT_TIME)