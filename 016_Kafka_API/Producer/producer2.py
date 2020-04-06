from time import sleep
from json import dumps
from flask import jsonify
import json
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers=['localhost:9096','localhost:9097','localhost:9098'])
artistid = "4r63FhuTkUYltbVAg5TQnk"
myheader = {"Authorization": "Bearer BQAFgBMscumGYbQTgVlAMEzOYe3BA4FyL0DnkzDnhB5um4THWBnVGV3DIone863QJc6Dfsk07-j2jyAmhHZVQxm3AL7XCR47bgNuncg6f6qCT7vWFxjHQOOc_ybG11FMHP7VlXOAK2ZuJFUkGo7so4qPGcAGafX5qToSrHtEmzWDdHHJOruilVAQuKY5OjJ8mijGZRmqNrzew3FQghA1oqlq_9dZXPkH3w2FLWKVBkEJxrMNPVWM5U9cCcFhC7q4Ehw9nAM8lo5_"}
PARAMS ={"ids":"4r63FhuTkUYltbVAg5TQnk"}
x = requests.get('https://api.spotify.com/v1/artists',params = PARAMS, headers = myheader)
print(x.text)
	


