from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from pyspark import sql
from pyspark.sql import SQLContext
from pyspark.sql import types
import json
from json import loads
from time import sleep
import pandas as pd
import sqlalchemy
import pymongo 

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["local"]
mycol = mydb["mycollection"]

sc =SparkContext()
ssc = StreamingContext(sc,4)

sqlContext = sql.SQLContext(sc)
directKafkaStream = KafkaUtils.createStream(ssc,"localhost:2181", "mygroup", {"sparky":1})

myrdd = directKafkaStream.map(lambda x: x)

def process_rdd(rdd):
	if not rdd.isEmpty():
		for x in rdd.collect():
			mylist = list(x[1].split("\n"))
			if (len(mylist) == 6):
				df = pd.DataFrame({'News_Type': mylist[0].encode('utf-8'), 'News_Snippets': mylist[1].encode('utf-8'), 'Date_Published': mylist[2].encode('utf-8'), 'Article_Type' :mylist[3].encode('utf-8'), 'Word_Count' :float(mylist[4].encode('utf-8')), 'Views' :float(mylist[5].encode('utf-8'))}, index=[0])
				print(df)
				mydic = {'News_Type': mylist[0], 'News_Snippets': mylist[1], 'Date_Published': mylist[2], 'Article_Type' :mylist[3], 'Word_Count' :float(mylist[4]), 'Views' :float(mylist[5])}
				x = mycol.insert_one(mydic)
			

	else:
		print("Is Empty")


myrdd.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
