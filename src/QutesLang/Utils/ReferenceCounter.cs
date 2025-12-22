namespace QutesLang.Utils;

public class ReferenceCounter<T> where T : notnull
{
    private readonly Dictionary<T, int> storage; // Key: element, Value: count

    public ReferenceCounter()
    {
        storage = [];
    }

    public ReferenceCounter(ReferenceCounter<T> counter)
    {
        storage = new Dictionary<T, int>(counter.storage);
    }

    public IEnumerable<T> Elements => storage.Keys;

    /// <summary>
    /// Adds an element. If it exists, increments the counter.
    /// </summary>
    public void Add(T item)
    {
        if (storage.TryGetValue(item, out int count))
        {
            storage[item] = count + 1;
        }
        else
        {
            storage[item] = 1;
        }
    }

    /// <summary>
    /// Decrements the counter. If it reaches zero, removes the element.
    /// Returns true if the decrement was successful, false if item was not found.
    /// </summary>
    public bool Remove(T item)
    {
        if (storage.TryGetValue(item, out int count))
        {
            if (count > 1)
            {
                storage[item] = count - 1;
            }
            else
            {
                storage.Remove(item);
            }
            return true;
        }
        return false;
    }

    public bool Contains(T item)
    {
        return storage.ContainsKey(item);
    }
}
