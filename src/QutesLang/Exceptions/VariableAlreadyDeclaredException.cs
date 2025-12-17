namespace QutesLang.Exceptions;

[Serializable]
internal class VariableAlreadyDeclaredException : Exception
{
    public VariableAlreadyDeclaredException()
    {
    }

    public VariableAlreadyDeclaredException(string? message) : base(message)
    {
    }

    public VariableAlreadyDeclaredException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}