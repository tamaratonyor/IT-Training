import socket
import sys
import requests
import requests_oauthlib
import json
from time import sleep

ACCESS_TOKEN = '559516596-yDA9xqOljo4CV32wSnqsx2BXh4RBIRKFxZGSZrPC'
ACCESS_SECRET = 'zDxePILZitS5tIWBhre0GWqps0FIj9OadX8RZb6w8ZCwz'
CONSUMER_KEY = 'uX0TWqkx0okYEjjqLzxIx6mD6'
CONSUMER_SECRET = 'rzHIs3TMJnADbZNvdGU7LQUo0kPxPISq3RGSLfqcBip39X5END'
my_auth = requests_oauthlib.OAuth1(CONSUMER_KEY, CONSUMER_SECRET,ACCESS_TOKEN, ACCESS_SECRET)

def get_tweets():
	url = 'https://stream.twitter.com/1.1/statuses/filter.json'
	query_data = [('language', 'en'), ('locations', '-130,-20,100,50'),('track','#2020Election','#Trump','#Biden')]
	query_url = url + '?' + '&'.join([str(t[0]) + '=' + str(t[1]) for t in query_data])
	response = requests.get(query_url, auth=my_auth, stream=True)
	print(query_url, response)
	return response

def send_tweets_to_spark(http_resp, tcp_connection):
	for line in http_resp.iter_lines():
		try:
			full_tweet = json.loads(line)
			tweet_text = full_tweet['text']
			tweet_time = full_tweet['created_at']
			dic = full_tweet['place']
			tweet_location = dic['full_name']
			print("Tweet Text: " + tweet_text)
			print("Tweet Time: " + tweet_time)
			print("Tweet Location: " + tweet_location)
			#mydic = {"Tweet": tweet_text.decode(), "Time": tweet_time.decode(), "Location": tweet_location.decode()}
			print ("---------------------------------------------------------------------")
			tcp_connection.send(tweet_text +"@#%%$"+tweet_time+"@#%%$"+tweet_location)
			tcp_connection.send("\n")
			sleep(3)
		except:
			e = sys.exc_info()[0]
			print("Error: %s" % e)


TCP_IP = "localhost"
TCP_PORT = 5555
conn = None
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
print("Waiting for TCP connection...")
conn, addr = s.accept()
print("Connected... Starting getting tweets.")
resp = get_tweets()
send_tweets_to_spark(resp, conn)




