namespace QutesLang.Symbols.Types.Interfaces;

public interface IClassicalValue : IQutesValue
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);
}