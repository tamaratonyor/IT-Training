import boto3
from time import sleep
from json import dumps
import json
import requests

client = boto3.client('kinesis')
shardlist = []
for x in range(10):
	PARAMS = {"fq":"Times","page":str(x), "fl":"news_desk,type_of_material,snippet,pub_date,word_count", "api-key":"02xPN9BcW56b7Vlf7WNzgAsOju7HOKdr"}
	x = requests.get('https://api.nytimes.com/svc/search/v2/articlesearch.json?',params = PARAMS)
	response = x.text
	shardlist.append(client.put_record(StreamName='NYSTREAM', Data=response.encode('utf-8'), PartitionKey='1'))
	print(response)
