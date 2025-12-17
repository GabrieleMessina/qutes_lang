namespace QutesLang.Exceptions;

[Serializable]
internal class VariableNotDeclaredException : Exception
{
    public VariableNotDeclaredException()
    {
    }

    public VariableNotDeclaredException(string? message) : base(message)
    {
    }

    public VariableNotDeclaredException(string? message, Exception? innerException) : base(message, innerException)
    {
    }
}