namespace QutesLang.Utils;

/// <summary>
/// adesso abbiamo che non è possibile referenziare/usare una variabile più di una volta nel contesto di un ciclo for parallel.
/// ma in realtà a noi importa che non si eseguano operazioni quantum più volta sulla stessa variabile.
/// o meglio che non ci siano operazioni quantistiche che coinvolgono registri già coinvoilti in altre operazioni.
/// come fare? il controllo va allora fatto al livello del circuit handler.
/// </summary>
/// <typeparam name="T"></typeparam>
public class AccessControlContext<T> where T : notnull
{
    private HashSet<T> AccessedElements = [];
    /// <summary>
    /// Registers the specified element as accessed in the current parallel context. Prevents multiple accesses to the
    /// same element within the same context.
    /// </summary>
    /// <param name="element">The element to register as accessed. Cannot be registered more than once in the same parallel context.</param>
    /// <exception cref="ParallelAccessViolationException">Thrown if the specified element has already been registered as accessed in the current parallel context.</exception>
    public void RegisterAccess(T element)
    {
        if (!AccessedElements.Add(element))
        {
            throw new ParallelAccessViolationException($"Try to manipulate element '{element}' multiple times in parallel context.");
        }
    }
    public void Reset()
    {
        AccessedElements = [];
    }
}
