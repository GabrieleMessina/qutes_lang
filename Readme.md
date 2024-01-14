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
    //This ifelse should create a controlled custom gate 
    if(grover_find()){
        //do quantum operations
    }
    else{
        //do other quantum operations
    }
    
    //This ifelse could convert all classical operations to quantum or cause a measure. 
    if(grover_find()){
        //do a mix of classical and quantum operations
    }
    else{
        //do other mix of classical and quantum operations
    }
```
## Explicit casting
```csharp
    quint a = 1q;
    qubit b = (qubit)a;
```
## Quantum types comparison
```csharp
    quint a = 0q;
    qubit b = (qubit)a;
    if(a){ //This should throw
    }
    if(b){ //This should be false
    }
    if(a > b){ //This and other comparing operator should be implemented for both qubit and quint
    }
```

## Handle quantum scope
```csharp

    //In this case we need to execute a piece of code in a quantum realm and another piece on a classical cpu before caming back to a quantum circuit.
    //It's not clear how we should handle this. Should this be transparent to the user? Should we make clearer that a measurement is needed to sum 'input' and 'x'
    {
        quint x = 10q;
        if(x > 0){
            string input = classical_read_user_input(); //just an explanatory example for a function that cannot run on a quantum circuit and must run on classic CPU.
            x += (int)input;
        }
        x = quantum_sqrt(x);
        measure x;
    }

    //This two blocks can be two different circuits.
    {
        qubit a = [true]q;
        qubit b = [true]q;
        quint x = a + b;
        measure x;
    }
    {
        quint a = 10q;
        quint d = 4q;
        quint re = a + c;
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
        quint b = 10q;
        quint re = b + a;
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

## Proof of concept
```csharp
    public qubit string_contains(qustring dataset, qustring query){
        //quantum circuit with rotation
    }

    //string where to search
    Qustring a = "lorem ipsum"q;
    
    //list of indexes where a substring "ore" starts
    Quint[] results = grover_find_results(string_contains(a, "ore"q));

    //print the founded results if any
    if(results.lenght > 0){
        print results; 
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
