namespace QutesLang.Utils;

public class AccessCounter
{
    private int counter = 0;

    public void Increment()
    {
        counter++;
    }

    public void Decrement()
    {
        if (counter > 0)
        {
            counter--;
        }
        else
        {
            throw new InvalidOperationException("Too many decrements. Counter cannot be negative.");
        }
    }

    public static implicit operator bool(AccessCounter accessCounter)
    {
        return accessCounter.counter > 0;
    }
}
