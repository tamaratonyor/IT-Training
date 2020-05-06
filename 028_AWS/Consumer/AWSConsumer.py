#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import boto3
from time import sleep
from json import dumps
import json
import requests
import pandas as pd
import sqlalchemy

database_username = 'admin'
database_password = 'Password123'
database_name = 'nydb'
database_ip       = 'nydb.cqdk5nbfyybo.us-east-2.rds.amazonaws.com'
database_port = '3306'

database_connection = sqlalchemy.create_engine('mysql+pymysql://admin:{0}@{1}/nydb?host={1}?port={2}'.
                                               format(database_password, database_ip, database_port))
client = boto3.client('kinesis')
listdic = []
sharditerator = client.get_shard_iterator(StreamName='NYSTREAM', ShardId='shardId-000000000000', ShardIteratorType= 'TRIM_HORIZON')
iterator = str(sharditerator[u'ShardIterator'])
while iterator is not None:
	response = client.get_records(ShardIterator= iterator)
	if not response[u'Records']:
		break
	
	else:
		myval = response[u'Records']
		for x in range(len(myval)):
			stringdic =  str(myval[x][u'Data'])
			if stringdic == None or stringdic == '':
  				print('Empty')
			else:
				mydic = json.loads(stringdic)
				entries = mydic["response"]["docs"]
				for y in entries:
					listdic.append(y)
					iterator = response[u'NextShardIterator']
	
for x in listdic:
	df = pd.DataFrame({'News_Type': x[u'type_of_material'].encode("utf-8"), 'News_Snippets': x[u'snippet'].encode("utf-8"), 'Date_Published': x[u'pub_date'].encode("utf-8"), 'Article_Type' : x[u'news_desk'].encode("utf-8"), 'Word_Count' :float(x[u'word_count'])}, index=[0])
	print(df)
	df.to_sql(con=database_connection, name='NY_TIMES', if_exists='append')



