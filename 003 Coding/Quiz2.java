import java.util.Scanner;
import java.util.ArrayList;

public class Word_Counter 
{

	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		System.out.print("Please enter your word");
		String s = in.nextLine();
		ArrayList<String> reverse = new ArrayList<String>();
		
		for (int i = s.length; i >= 0; i--)
		{
			reverse.add(s.charAt(i));
		}
		for (int i = 0; i < reverse.size(); i++) 
		System.out.print(+reverse(i));
		
	}

}
