from kafka import KafkaConsumer
from json import loads
from pyarrow import hdfs

consumer = KafkaConsumer( 'bigData', bootstrap_servers=['localhost:9096','localhost:9097','localhost:9098'], auto_offset_reset='earliest',group_id='group_1')
hdfs = hdfs.connect('localhost', 9000,'tammy',driver='libhdfs')
path = '/kafkatest/hdfs_kafka.txt'
f = hdfs.open(path, 'wb')
for message in consumer:
	message = message.value
	f.write(str(message.decode("utf-8")))

f.close()

