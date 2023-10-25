# Language Design

## Atomic Operators
- h (h gate)
- not (pauli-x or x gate)
- notPhase (pauli-z or z gate)
- pauli-y (pauli-y or y gate)
- c-op (controlled gates)
- m-op (multiple controlled gates)

## Simple Operators
- and
- or
- xor
- swap
- correlate

## Complex Operators
- \+ (sum gate)
- == (compare gate)
- = (assign or copy gate)

## Data types
- bit
- byte
- bool
- int16/32/64 (or generic number?)
- uint16/32/64 (or generic number?)
- float (or generic number?)
- double (or generic number?)
- string

> We should consider handle the difference between classical type variable and quantum type variable.

## What we'd like to achieve
Here some example of what the syntax should look like and also what the capabilities of the language should be. 

### Sommare due interi (lower level)
```csharp
public int Sum(bit a, bit b){
    //1. convert the int rappresentatin to a qbit or bit one
    //2. create the quantum cicuits with qiskit or qasm
    //3. measure and return the value

    qbit _a = new qbit(a);
    qbit _b = new qbit(b);
    qbit _sum = new qbit();
    qbit _carry = new qbit();

    { //Some ideas for implements a low lever controlled not gate
        //Option1
        _a cx _sum;
        //Option1 bis
        _a !=> _sum;
        //Option2
        if(_sum){
            _a = not _a;
        }
        //Option3
        cx(_a, _sum)
        //Option4
        negate _sum when _a;
        //Option4 bis
        not _sum when _a;
    }

    negate _sum when _a;
    negate _sum when _b;
    negate _carry when _a and _b;
    bit res0 = measure _sum;
    bit res1 = measure carry;

    return res0 + res1 * 2;
}
```

### Sommare due interi (higher level)
```csharp
public void Sum(int a, int b){
    //1. convert the int rappresentatin to a qbit or bit one
    //2. create the quantum cicuits with qiskit or qasm
    //3. measure and return the value

    qint _a = new qint(a);
    qint _b = new qint(b);

    qint quantum_result = _a + _b;
    int result = measure(quantum_result);
    return result;
}
```

### Eguagliare due interi
```csharp
public void Equals(int a, int b){
    //1. convert the int rappresentatin to a qbit or bit one
    //2. create the quantum cicuits with qiskit or qasm
    //3. measure and return the value
}
```