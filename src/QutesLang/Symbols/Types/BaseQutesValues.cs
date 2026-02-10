using System.Runtime.CompilerServices;

using QutesLang.QuantumCircuits;
using QutesLang.QuantumCircuits.Operations;
using QutesLang.Symbols.Types.Interfaces;

namespace QutesLang.Symbols.Types;

public abstract class OperableValue : IOperableValue
{
    protected OperableValue()
    {
        RegisterFunctions();
    }

    public abstract TypeSymbol Type { get; }
    public virtual Dictionary<string, FunctionValue> Functions { get; } = [];
    protected virtual void RegisterFunctions(){}
    public abstract bool TryConvertTo(TypeSymbol targetType, out IQutesValue result);

    public virtual QutesResult Addition(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Addition)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult And(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(And)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Divide(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Divide)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Equals(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Exp(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult GreaterEqualThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult GreaterThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult InplacePostDecrement() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult InplacePostIncrement() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult InplacePreDecrement() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult InplacePreIncrement() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult LeftShift(IQutesValue positions) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {positions.Type}.");

    public virtual QutesResult LowerEqualThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult LowerThan(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Minus() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult Module(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Multiply(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Not() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult NotEquals(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Or(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Plus() => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type}.");

    public virtual QutesResult RightShift(IQutesValue positions) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {positions.Type}.");

    public virtual QutesResult Subtraction(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");

    public virtual QutesResult Swap(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}.");
    public virtual QutesResult CNot(IQutesValue term) => throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {Type} and {term.Type}."); //TODO: implement in concrete classes.
}

public abstract class ClassicalValue : OperableValue, IClassicalValue
{
    public abstract object GetValueAsObject();
    public abstract void SetValueFromObject(object value);

    public override string ToString()
    {
        return $"{GetValueAsObject()}";
    }

    public override QutesResult Swap(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Cannot swap different types: {this.Type} and {term.Type}");

        var classicalValue = term.As<IClassicalValue>();
        var temp = this.GetValueAsObject();
        this.SetValueFromObject(classicalValue.GetValueAsObject());
        classicalValue.SetValueFromObject(temp);
        return this;
    }

    public override QutesResult Equals(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");

        var classicalValue = term.As<IClassicalValue>();
        var a = this.GetValueAsObject();
        var b = classicalValue.GetValueAsObject();
        return new BoolValue(a.Equals(b));
    }
    public override QutesResult NotEquals(IQutesValue term)
    {
        if (this.Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");

        var classicalValue = term.As<IClassicalValue>();
        var a = this.GetValueAsObject();
        var b = classicalValue.GetValueAsObject();
        return new BoolValue(a.Equals(b) == false);
    }

    public override QutesResult Plus() => this;
}

public abstract class QuantumValue : OperableValue, IQuantumValue
{
    public int QubitCount => Register.Size;
    public abstract QuantumRegister Register { get; protected set; }
    public abstract override TypeSymbol Type { get; }
    public string QubitStringList => Register.QubitStringList;

    public override string ToString()
    {
        return $"({Type}) {Register}";
    }

    public static IQuantumValue GetQuantumValue(IQutesValue term, [CallerMemberName] string operationName = "")
    {
        if (term is not IQuantumValue quantumValue)
            throw new InvalidOperationException($"Operation {operationName} cannot be applied to {term.Type} type.");

        return quantumValue;
    }

    public override QutesResult Swap(IQutesValue term)
    {
        if (Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Swap)} cannot be applied to {this.Type} and {term.Type}.");

        var quantumValue = term.As<IQuantumValue>();
        return new Swap(this, quantumValue);
    }

    public override QutesResult Equals(IQutesValue term)
    {
        if (Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(Equals)} cannot be applied to {this.Type} and {term.Type}.");

        var quantumValue = term.As<IQuantumValue>();
        return new Equals(this, quantumValue, new QubitValue());
    }

    public override QutesResult NotEquals(IQutesValue term)
    {
        if (Type != term.Type)
            throw new InvalidOperationException($"Operator {nameof(NotEquals)} cannot be applied to {this.Type} and {term.Type}.");

        var quantumValue = term.As<IQuantumValue>();
        return new NotEquals(this, quantumValue, this);
    }

    public override QutesResult Plus() => new Empty(this);
}

public abstract class ArrayValue : OperableValue
{
    /// <summary>
    /// Array elements, this cannot be a list of IQutesValue because we need to store also the symbol information,
    /// otherwise, we wouldn't be able to return a unique symbol when array is accessed.
    /// </summary>
    public abstract IEnumerable<ValueSymbol> Values { get; protected set; }

    public int Count => Values.Count();

    protected override void RegisterFunctions()
    {
        base.RegisterFunctions();
        Functions["length"] = new FunctionValue(args => new IntValue(Values.Count()));
    }

    public override bool TryConvertTo(TypeSymbol targetType, out IQutesValue result)
    {
        if (Type == targetType)
        {
            result = this;
            return true;
        }
        else
        {
            var newArray = CastAllElementsToType(targetType.NestedValue!);
            result = newArray;
            return true;
        }
    }

    private ArrayValue CastAllElementsToType(TypeSymbol elementsType)
    {
        var castedValues = new List<ValueSymbol>();
        foreach (var symbol in Values)
        {
            if (symbol.Value.TryConvertTo(elementsType, out var castedValue))
            {
                castedValues.Add(new AnonymousValueSymbol(castedValue, null!, default)); //TODO: check scope and astTokenIndex how to handle here. And if really necessay in general.
            }
            else
            {
                throw new InvalidCastException($"Cannot cast value of type {symbol.Type} to {elementsType}");
            }
        }

        if (elementsType.IsQuantum())
        {
            return new QuantumArrayValue(castedValues, elementsType);

        }
        else
        {
            return new ClassicalArrayValue(castedValues, elementsType);
        }
    }

    public override string ToString()
    {
        return "[" + string.Join(", ", Values) + "]";
    }
}