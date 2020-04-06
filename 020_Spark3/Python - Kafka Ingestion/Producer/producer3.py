from time import sleep
from json import dumps
import json
from kafka import KafkaProducer
import requests

producer = KafkaProducer(bootstrap_servers=['localhost:9091'])
artistid = "4r63FhuTkUYltbVAg5TQnk"
myheader = {"Authorization": "Bearer BQBsg5mNvH8fXTjhzJ4phIxf5yOX92tz6jQbMSl2LU10ybRX4--jNIAfALhpYXY7zTbLWamkSyGTMnZ71yr1Er_LUxGkCFnRQj0k1WTSlRpKP3e7x8gWOimd4VJ6l8Z7UnsJph5IW6iF4SKCu1Q4MZKxuOU0P_gW8cEhXveww1KLqBCg8Qtg_LCQyhcI0x_9RERzBwNE24mgL75145OywpwArCssdtrVYICqCSVSsMWVmTWzfgwksHteoLUjpSAe7rTjWZ5yjCdN"}
PARAMS ={"ids":"4r63FhuTkUYltbVAg5TQnk"}
x = requests.get('https://api.spotify.com/v1/artists',params = PARAMS, headers = myheader)
response = x.text
responselist = response.splitlines()

print (x.text)

for s in range(10): 
	producer.send('sparky', (x.text).encode('utf-8'))
	print("SUCCESS")



