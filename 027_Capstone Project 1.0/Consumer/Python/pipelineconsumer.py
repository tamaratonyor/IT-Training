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

database_username = 'tammy1'
database_password = 'Password@123'
database_ip       = 'localhost'
database_name     = 'bigData'
database_connection = sqlalchemy.create_engine('mysql+mysqlconnector://{0}:{1}@{2}/{3}'.
                                               format(database_username, database_password, 
                                                      database_ip, database_name))

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
				df = pd.DataFrame({'News_Type': mylist[0], 'News_Snippets': mylist[1], 'Date_Published': mylist[2], 'Article_Type' :mylist[3], 'Word_Count' :float(mylist[4]), 'Views' :float(mylist[5])}, index=[0])
				sdf = sqlContext.createDataFrame(df)
				sdf.show()
				df.to_sql(con=database_connection, name='NY_TIMES', if_exists='append')

	else:
		print("Is Empty")


myrdd.foreachRDD(process_rdd)

ssc.start()
ssc.awaitTermination()
