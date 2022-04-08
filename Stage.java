	/*
	 * Stage
	 * Created by Mohamed Hegazy
	 * Last updated by Mohamed Hegazy - 4/8/2022
	 * 
	 */
	 
	 
public class Stage extends InfoRecord
{
	public static void main(String args[])
	{
		Stage s = new Stage("Loading...");
		System.out.println(s.stringValue());
	}
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