import org.apache.kafka.clients.producer._
import java.util.Properties
import scalaj.http._
import scalaj.collection.Imports._
import scala.collection.mutable.ListBuffer
import scala.collection.mutable.Map
import play.api.libs.json._

object producer
{	
	
	def main(args: Array[String]): Unit =
	{
		val  props = new Properties()
 		props.put("bootstrap.servers", "localhost:9091")
 		props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer")
 		props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer")
		props.put("group.id", "mygroup")
		val producer = new KafkaProducer[String,String](props)
		val TOPIC = "sparky"
		for (x<- 1 to 100)
		{ 
			var response: HttpResponse[String] = Http("https://api.nytimes.com/svc/search/v2/articlesearch.json?").params(("fq","New York Times"),("page",x.toString),("fl","news_desk,type_of_material,snippet,pub_date,word_count"),("api-key","02xPN9BcW56b7Vlf7WNzgAsOju7HOKdr")).asString
			var json: JsValue = Json.parse(response.body)
			var desk = (json \\ "news_desk").map(_.as[String])
			var snippets = (json \\ "snippet").map(_.as[String])
			var dates = (json \\ "pub_date").map(_.as[String])
			var material = (json \\ "type_of_material").map(_.as[String])
			var words = (json \\ "word_count").map(_.as[Double])
			if (!desk.isEmpty)
			{ 
				for (i <- 0 until 10)
				{
					var strVal = desk(i)+"\n"+snippets(i)+"\n"+dates(i)+"\n"+material(i)+"\n"+words(i).toString+"\n"+(words(i)*4957).toString
					var record = new ProducerRecord(TOPIC,"",strVal)
					producer.send(record)

				}
			}

		}
		producer.close()	
	}
}
