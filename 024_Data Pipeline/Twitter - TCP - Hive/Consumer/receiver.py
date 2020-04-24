from pyspark import SparkConf,SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row,SQLContext,DataFrameWriter
from pyspark.sql import HiveContext
import sys
import json
import requests
import pandas as pd
from pyspark.sql.types import *
from pyspark.sql import SparkSession

conf = SparkConf()
conf.setAppName("TwitterStreamApp")
sc = SparkContext(conf=conf)
sc.setLogLevel("ERROR")
ssc = StreamingContext(sc, 3)
mylist = []
dataStream = ssc.socketTextStream("localhost",5555)
sqlcontext = HiveContext(sc)

def process_rdd(rdd):
	if not rdd.isEmpty():
		for x in rdd.collect():
			mylist = list(x.split("@#%%$"))
			if (len(mylist) == 3):
				df = pd.DataFrame({'Tweet': mylist[0], 'Time': mylist[1], 'Location': mylist[2]}, index=[0])
				sdf = sqlcontext.createDataFrame(df)
				sdf.show()
				sdf.registerTempTable("temptable") 
				sqlcontext.sql("CREATE TABLE IF NOT EXISTS mytable as select * from temptable")
	else:
		print("Is Empty")

print("mapping occurring----------------------")
myrdd = dataStream.map(lambda x: x)
print("mapping done---------------------------")
print("RDD beginning")
myrdd.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
