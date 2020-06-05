import org.apache.spark.streaming.StreamingContext._
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.sql._
import org.apache.spark.sql.types._
import org.apache.spark.streaming.kafka._
import java.util.Properties
import org.apache.spark.sql.SparkSession
import org.apache.spark.SparkConf
import scala.collection.mutable.ListBuffer

object consumer
{	
	def main(args: Array[String]): Unit =
	{
		val linelist: ListBuffer[String] = new ListBuffer[String]();
		val conf = new SparkConf()
		val ss = SparkSession.builderbuilder.master("local").appName("NYTimes").config("spark.cassandra.connection.host","localhost").config("spark.cassandra.connection.port", "9042").getOrCreate()
		import ss.implicits._
		val sc = ss.sparkContext
 		val ssc = new StreamingContext(sc, Seconds(5))
		val sqlContext = new org.apache.spark.sql.SQLContext(sc)
		val dstream = KafkaUtils.createStream(ssc, "localhost:2181", "mygroup" , Map("sparky"-> 1))
		val prop = new Properties()
		prop.setProperty("user", "tammy1")
		prop.setProperty("password", "Password@123")
		val schema = new StructType()
  		.add(StructField("News Type", StringType, false))
  		.add(StructField("News Snippets", StringType, false))
  		.add(StructField("Date Published", StringType, false))
		.add(StructField("Article Type", StringType, false))
		.add(StructField("Word Count", StringType, false))
		.add(StructField("Views", StringType, false))
		val mappedlines = dstream.foreachRDD{ rdd =>
      		rdd.foreach{record =>
			     var mylist = (record._2).split("\n")
			     print(mylist)
			     var myrdd = sc.parallelize(mylist)	
			     var df1 = myrdd.toDF()
			     // Create DF1 using toDF() created for my learning purpose	     
			     var myrdd2 = myrdd.map{x => Row(x(0),x(1),x(2),x(3),x(4),x(5))}
			     var df2 = sqlContext.createDataFrame(myrdd2, schema)
			     // Create DF2 using createDataframe, this DF is writtern to MYSQL
			     if (df1 !=null && df2 != null)
			     {
				df1.write.format("org.apache.spark.sql.cassandra").options(Map("table"->"Articles","keyspace" -> "Capstone")).mode(SaveMode.Append).save()
			     }
			   }
			println("RDD END IN STREAM!!!")
			println("RDD END IN STREAM!!!")
		}
		ssc.start
   		ssc.awaitTermination
	}
}
