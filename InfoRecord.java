	/*
	 * InfoRecord
	 * Created by Mohamed Hegazy
	 * Last updated by Mohamed Hegazy - 4/8/2022
	 * 
	 */
	 
	 
import java.util.regex.Matcher;
import java.util.regex.Pattern;


class Stage extends InfoRecord
{
	public Stage(String text, char block, int width)
	{
		super(10,block,"",((width-text.length())/2)+text.length()+(width%2==0?text.length()%2:0));
		setRecord(text, "");
	}
	public Stage(String text, int width)
	{
		this(text,'=',width);
	}
	public Stage(String text)
	{
		this(text,text.length()-(text.length() % 100)+100);
	}	
}

public class InfoRecord {
	private StringBuffer stringValueBuffer = new StringBuffer("");
	private String topTitle;
	private  int titleMaxLength;
	private  int indentLength;
	private  char block;
	private int padding = 0; //4+value.length()+(2*titleMaxLength)-title.length()-topTitle.length
	
	public static void main(String args[])
	{
		InfoRecord r = new InfoRecord();
		r.setRecord("Name","InfoRecord");
		r.setRecord("Language","Java");
		r.setRecord("Description","Simple class for convenient text display\n....\n...");
		System.out.println(r.stringValue());
		Stage s = new Stage("Loading...");
		System.out.println(s.stringValue());
		
	}
	
	private StringBuffer appendRightBlocks(StringBuffer input)
	{
		Pattern p = null;
		Matcher currentMatcher;
		StringBuffer tempBuffer = null;
		p = Pattern.compile("[\r\n][ ]*(["+block+"].*)");
		currentMatcher = p.matcher(input);
		tempBuffer = new StringBuffer();
		while(currentMatcher.find())
		{
			currentMatcher.appendReplacement(tempBuffer,currentMatcher.group(0)+padding((2*padding+topTitle.length())-(currentMatcher.group(1).replace("$","").replace("\\\\","\\").length())-1,' ')+block);
		}
		currentMatcher.appendTail(tempBuffer);
		return tempBuffer;
	}
	protected void setRecord(String title, String value)
	{
		try
		{
			String[] tokens = value.replaceAll("\t", " ").split("[\n\r]");
			for (int i=0 ; i< tokens.length ; i++)
			{
				stringValueBuffer.append("\n");
				stringValueBuffer.append(padding(indentLength,' '));
				stringValueBuffer.append(block);
				stringValueBuffer.append(padding(titleMaxLength-title.length(),' '));
				stringValueBuffer.append(i==0?title:padding(title.length(),' '));
				stringValueBuffer.append(i==0&&!value.equals("")?" : ":"   ");
				stringValueBuffer.append(Matcher.quoteReplacement(tokens[i]));
				calcPadding(title, tokens[i]);
			}
		}
		catch(Exception e)
		{
			System.out.println("An Unexpected Exception Occured");
		}
	}
	private void calcPadding(String title, String value)
	{
		int newPadding = (4+value.length()+(2*titleMaxLength)-title.length()-topTitle.length())/2;
		padding = padding<newPadding?newPadding:padding;
	}
	private String padding(int r, char x)
	{
		StringBuffer b = new StringBuffer();
		for(int i=0 ; i<r ; i++)
		{
			b.append(x);
		}
		return b.toString();
	}
	private String header()
	{
		return 	"\n"+padding(indentLength,' ')+
				padding(padding, block)+
				topTitle+
				padding(padding, block);
	}
	private String footer()
	{
		return "\n"+padding(indentLength,' ')+
				padding((2*padding)+topTitle.length(), block)+
				"\n\n";
	}
	protected InfoRecord()
	{
		indentLength = 20;
		block = '+';
		topTitle = ": System Data :";
		titleMaxLength = 25;
	}
	protected InfoRecord(int indentLength, char block, String topTitle, int titleMaxLength)
	{
		this.indentLength = indentLength;
		this.block = block;
		this.topTitle = topTitle;
		this.titleMaxLength = titleMaxLength;
	}
	public String stringValue()
	{
		String returnValue = "";
		returnValue+=header();
		try
		{
			returnValue+=appendRightBlocks(stringValueBuffer);
		}
		catch(Exception e)
		{}
		returnValue+=footer();
		return returnValue;
	}
}
