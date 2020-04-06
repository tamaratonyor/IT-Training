import org.apache.spark.streaming.flume._
import org.apache.spark.streaming.StreamingContext._
import org.apache.spark.streaming.Seconds
import org.apache.spark._
import org.apache.spark.streaming._
import org.apache.spark.sql._
import org.apache.spark.sql.types._
import scala.collection.mutable.ListBuffer

object Consumer3A 
{
 val context = new SparkContext()
 val ssc = new StreamingContext(context, Seconds(5))
 val flumeStream = FlumeUtils.createPollingStream(ssc, "localhost", 4333)
 val sqlContext = new org.apache.spark.sql.SQLContext(context)
 val schema = StructType(
     StructField("Time", StringType) ::
     StructField("Tweet", StringType) ::
     StructField("Location", StringType) :: Nil)

 def main(args: Array[String]): Unit =
	{	
		val lines = flumeStream.map{e => new String(e.event.getBody().array(), "UTF-8")}
		lines.foreachRDD{ rdd =>
  				rdd.foreach { record =>
    				print(record)
  					     }
				val row = rdd.map(p => Row(p(0), p(1)))
				val df = sqlContext.createDataFrame(row, schema)
				df.show()
				}

		ssc.start
   		ssc.awaitTermination
	}

}
