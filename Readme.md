# Qutes Lang
A high level programming language for quantum computing.

# Implemented Features
## Variable Declaration and Assignment
```csharp
    bool a = true;
    int b = 10;
    string c = "Hello";
    qubit d = 1q;
    quint e = 10q;
```

## Variable Scope
```csharp
    bool b = false;
    {
        int b = 100; //this int b override the upper bool b.  
    }
    b = true; //this b refer to the bool b.
```

## Printing
```csharp
    int a = 10;
    quint b = 10q;
    print b;
```

## Branching
```csharp
    bool b = true;
    if(b){
        //Do something.
    }

    if(!b){
        //Do something.
    }
    else{
        //Do something else.
    }

    if(b){
        //Do something.
    }
    else if(true){
        //Do something else.
    }
```

## Looping
```csharp
    bool b = true;
    while(b){
        //Do something while b == true.
        b = false;
    }

    do{
        //Do something until b == false.
        b = true;
    }
    while(!b)
```

## Qubit declaration syntax
```csharp
    //alpha and beta values
    qubit a = 0.7,0.3q;
    //states we want the qubit is able to take
    qubit b = [0, 1]q;
    //shorter syntax for a qubit that take only the zero value
    qubit c = 0q;
    //special syntax for common superposition
    qubit d = |+>;
    qubit e = |->;
```

## Quint declaration syntax
```csharp
    //quint with 2^4 qubits that represent the number 10.
    quint a = 10q;
    //quint representing the number 1
    quint b = [0q, 0q, 1q]; 
    //quint with a superposition state where the most significant bit can be 0(70%) or 1(30%)
    quint c = [0.7,0.3q, 0q, 1q];
    //quint with a superposition state where the most significant bit can be 0(50%) or 1(50%) 
    quint d = [[0, 1]q, 0q, 1q];
    //quint with a superposition state that can be both 1(50%) or 3(50%)
    quint e = [1, 3]q; 
```

## Quantum basic operations
```csharp
    qubit a = 1q;
    qubit b = 1q;
    not a;
    pauliz a;
    hadamard a;
    quint c = a + b;
```

## Quantum circuit measurement
```csharp
    //Explicit measure
    qubit a = [1]q;
    qubit b = [1]q;
    quint x = a + b;
    measure x;

    //Implicit measure
    qubit a = [true]q;
    qubit b = [true]q;
    int classical = a + b;
```

# Features to implement
## Branching on quantum functions and/or a mix of quantum and classical operations
```csharp
    if(grover_find()){
        //do something
    }
    else{
        //do something else
    }
```
## Explicit casting
```csharp
    quint a = 1q;
    qubit b = (qubit)a;
```

## Handle quantum scope
```csharp
    //This two blocks can be two different circuits.
    {
        qubit a = [true]q;
        qubit b = [true]q;
        quint x = a + b;
        measure x;
    }
    {
        quint c = 10q;
        quint d = 4q;
        quint re = d + c;
        measure re;
    }

    //-----------

    //This two blocks cannot be two different circuits because they use the same global variable.
    //But we can say that we have two custom gate in the circuit,
    //So if a custom gate doesn't take anything as input then it's a new circuit.
    qubit a = [1]q;
    {
        qubit b = [1]q;
        quint x = a + b;
        measure x;
    }
    {
        quint c = 10q;
        quint re = c + a;
        measure re;
    }
```

## Functions
```csharp
    //easy to implement, create a new variable scope and execute the code inside.
    public int sum(int a, int b){
        return a + b;
    }

    //This could be implemented as a custom gate of the quantum circuit, but we need to handle the parameters allocation, release and the scope of the variables.
    public quint sum(quint a, quint b){
        return a + b;
    }
```

## How to Run
### 1. Install python requirements
```bash
pip install -r requirements.txt --upgrade
```
### 2. Compile the antlr grammar
With [this](https://marketplace.visualstudio.com/items?itemName=mike-lischke.vscode-antlr4) antlr VS Code extension, or:
```bash
antrl4 -Dlanguage=Python3 -message-format antlr -o ./src/qutes_antlr -listener -visitor -Xexact-output-dir ./specification/grammar/qutes_lexer.g4

antrl4 -Dlanguage=Python3 -message-format antlr -o ./src/qutes_antlr -listener -visitor -Xexact-output-dir ./specification/grammar/qutes_parser.g4
```
### 3. Compile the Qutes source code
```bash
python ./src/qutes.py ./specification/grammar/grammar_test.qut
```

### Notes
You can follow the official antlr repository [starting guide for Python](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) if you need a help getting the environment ready.
