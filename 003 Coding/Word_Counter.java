import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import java.io.File;  // Import the File class 
import java.util.Scanner; // Import the Scanner class to read text files

public class Word_Counter {

	public static void main(String[] args)
	{
	  try
		{
			File myObj = new File("/home/fieldemployee/Downloads/Shakespeare.txt");
			Scanner myReader = new Scanner(myObj);
			ArrayList<String> Line = new ArrayList<String>();
	        ArrayList<String> word = new ArrayList<String>();
			while (myReader.hasNextLine()) 
			{
		        Line.add( myReader.nextLine().toString());
		        for(int i =0; i<Line.size(); i++)
		        	{
		        		word.add(Line.get(i).split(" ").toString());
		        	}
		       
			}
		
			HashMap<String, Integer> map = new HashMap<String, Integer>();
			for (String str : word)
			{
				if (map.containsKey(str))
				{
					map.replace(str,map.get(str)+1);
				}
				else
				{
					map.put(str,1);
				}
				
			}
			
			System.out.print(map);
			myReader.close();
			
		}
		catch (FileNotFoundException e)
		{
			System.out.print("There was an error");
		}
	}
}
