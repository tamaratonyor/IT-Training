
object Counter {
  def main(args: Array[String]): Unit =
  {
    var numList: List[Int] = List()
    for (x <- 0 until 30)
    {
      val numList[x] = scala.util.Random.nextInt()
    }

     def nameAndID(name: String, ID: String): String =
    {
	      return name+ID
    }
    nameAndID("Carl","123")
    
    def removeDuplicates(objectList: List[String]):List[String] = {
       for (x <- 0 until objectList.length)
       {
         for (j<- 1 until objectList.length)
         {
            if (objectList[j] == objectList[x])
           {
             objectList[j] = ""
           }
         } 
       }
     }
  
     def smallestMissingInteger(numList: List[Int]):Int = {
       for (x <- 0 until numList.length)
       {
          if (numList[x] < 0)
	  {
		while (numList[x] < 0)
		{
		  numList[x]+=1
		}
            if (!numList.contains(numList[x]))
	    {
	      return numList[x]
            }
	  }
       }
     }

  }
}


