namespace QutesLang.Exceptions;

[Serializable]
internal class ParallelAccessViolationException : Exception
{
    public ParallelAccessViolationException()
    {
    }

    public ParallelAccessViolationException(string? message) : base(message)
    {
    }

    public ParallelAccessViolationException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}