import datetime as dt
from time import sleep
from json import dumps
import json
from pyspark.streaming.kafka import KafkaUtils
from kafka import KafkaProducer
from pyspark.streaming import StreamingContext
from pyspark import SparkContext
from pyspark import SparkConf
from pyspark import sql
from pyspark.sql import SQLContext
from pyspark.sql import types
import csv
from json import loads
from flatten_json import flatten
import pandas as pd
import requests
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator


def producer():
	producer = KafkaProducer(bootstrap_servers=['localhost:9091'])
	artistid = "4r63FhuTkUYltbVAg5TQnk"
	myheader = {"Authorization": "Bearer BQB86WZ_5wl7kGWgBAw4hedbvezdzm2z4F48rzVnpCf1cT0JZfQ9bVexwneB3A0pVRCfE0jlUjKHV0sGXElITfJ0cQaLrHiGzPuAyEKtAWZ4TPCu-rsNZelDtfTqgJfMDeRwwezBxK6ue2kyg3eV61uoJhjuZgRoiKgw3ih9bSBw2i4-GJ1m1UjPSiHMmGBvld3YMuC-57GDeYK3OxMFcH3K3VMaGAhw8ig_cPwbzW02VqP5wwLj32pQ-y8ZeZ-874u7uE-d4qE3"}
	PARAMS ={"ids":"4r63FhuTkUYltbVAg5TQnk"}
	x = requests.get('https://api.spotify.com/v1/artists',params = PARAMS, headers = myheader)
	response = x.text
	responselist = response.splitlines()

	print (x.text)

	for s in range(10): 
		producer.send('sparky', (x.text).encode('utf-8'))
		print("SUCCESS")


def consumer():
	conf = SparkConf().set("spark.jars", "/home/tammy/Downloads/spark-streaming-kafka-0-8-assembly_2.11-2.4.4.jar")
	sc =SparkContext(conf=conf)
	ssc = StreamingContext(sc,5)
	print("PROGRAM STARTING!!!!!!!!!")
	print("PROGRAM STARTING!!!!!!!!!")

	sqlContext = sql.SQLContext(sc)
	directKafkaStream = KafkaUtils.createDirectStream(ssc, ["sparky"], {"metadata.broker.list":
"localhost:9091"})
	lines = directKafkaStream.map(lambda x: x[1])
	line_list = []

	def makeIterable(rdd):
		for x in rdd.collect():    
			print(x)
			line_list.append(x)
			strippedlist = [sub.replace('\n', '').replace('\r','').replace(' ','') for sub in line_list] 
			dic = json.loads(strippedlist[0])
			flattened_list = [flatten(dic)]
			df = pd.DataFrame(flattened_list)
			print(df)


	lines.foreachRDD(makeIterable)


	ssc.start()
	ssc.awaitTermination()



default_args = {
    'owner': 'tammy',
    'start_date': dt.datetime(2020, 4, 17),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}



with DAG('airflow_tutorial_v01',
         default_args=default_args,
         schedule_interval='0 * * * *',
         ) as dag:

    producer = PythonOperator(task_id='producer',
                               python_callable=producer)
    consumer = PythonOperator(task_id='consumer',
                                 python_callable=consumer)


producer >> consumer



