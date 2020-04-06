from pyspark.streaming.kafka import KafkaUtils
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from pyspark import sql
from pyspark.sql import SQLContext
from pyspark.sql import types
import json
import csv
from json import loads
from flatten_json import flatten
from time import sleep
import pandas as pd


sc =SparkContext()
ssc = StreamingContext(sc,5)

print("PROGRAM STARTING!!!!!!!!!")
print("PROGRAM STARTING!!!!!!!!!")
print("PROGRAM STARTING!!!!!!!!!")
print("PROGRAM STARTING!!!!!!!!!")
print("PROGRAM STARTING!!!!!!!!!")
print("PROGRAM STARTING!!!!!!!!!")
sqlContext = sql.SQLContext(sc)
directKafkaStream = KafkaUtils.createDirectStream(ssc, ["sparky"], {"metadata.broker.list": "localhost:9091"})
sleep(3)
lines = directKafkaStream.map(lambda x: x[1])
line_list = []


def makeIterable(rdd):
	for x in rdd.collect():    
		print(x)
		line_list.append(x)
		sleep(1)
		strippedlist = [sub.replace('\n', '').replace('\r','').replace(' ','') for sub in line_list] 
		dic = json.loads(strippedlist[0])
		flattened_list = [flatten(dic)]
		df = pd.DataFrame(flattened_list)
		print(df)


lines.foreachRDD(makeIterable)


ssc.start()
ssc.awaitTermination()



