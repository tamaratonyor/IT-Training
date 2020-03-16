import java.util.Scanner;
import java.util.ArrayList;

public class Word_Counter 
{

	public static void main(String[] args)
	{
		Scanner input = new Scanner(System.in);
		System.out.print("Please enter your word");
		String s = input.nextLine();
		char[] reverse = new char[s.length()];
		
		for (int i = s.length()-1; i >= 0; i--)
		{
		    int j = 0;
			reverse[i] = s.charAt(j);
			j++;
		}
		for (int i = 0; i < reverse.length; i++) 
		System.out.print(+reverse[i]);
		
	}

}
