# Qutes Lang
A **High Level programming language** for **quantum computing** that allows **everyone**, even those who do not know the theory behind quantum computing in detail, **to exploit its potential** and adapt it to their field of interest.

[![Qutes Build and Tests](https://github.com/GabrieleMessina/qutes_lang/actions/workflows/python-app.yml/badge.svg)](https://github.com/GabrieleMessina/qutes_lang/actions/workflows/python-app.yml)
[![Codespaces Prebuilds](https://github.com/GabrieleMessina/qutes_lang/actions/workflows/codespaces/create_codespaces_prebuilds/badge.svg)](https://github.com/GabrieleMessina/qutes_lang/actions/workflows/codespaces/create_codespaces_prebuilds)
## How to Run - 🧭 Easy Start
> [!TIP]
> You can use a GitHub Codespace to start work with Qutes quickly.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/GabrieleMessina/qutes_lang?quickstart=1)

Everything will be already settled, you just need to open the VSCode Workspace when requested and run the code from the Debug panel.

If needed, remember to update the code with a Git Pull command!

## How to Run - 🛠️ On your own Environment
### 1. Install python requirements
```bash
pip install -r requirements.txt --upgrade
```
### 2. Compile the Qutes source code
```bash
python ./src/qutes.py ./specification/grammar/grammar_test.qut
```

## 🗺️ Implemented Features
### Variable Declaration and Assignment
```csharp
bool a = true;
int b = 10;
string c = "Hello";
qubit d = 1q;
quint e = 10q;
```

### Variable Scope
```csharp
bool b = false;
{
    int b = 100; //this int b overrides the upper bool b.  
}
b = true; //this b refers to the bool b.
```

### Printing
```csharp
int a = 10;
quint b = 10q;
print b;
```

### Branching
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

### Looping
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

### Qubit declaration syntax
```csharp
//alpha and beta values
qubit a = 0.7,0.3q;
//states we want the qubit to be able to take
qubit b = [0, 1]q;
//shorter syntax for a qubit that takes only the zero value
qubit c = 0q;
//special syntax for common superposition
qubit d = |+>;
qubit e = |->;
```

### Quint declaration syntax
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

### Quantum basic operations
```csharp
qubit a = 1q;
qubit b = 1q;
not a;
pauliz a;
hadamard a;
quint c = a + b;
```

### Quantum circuit measurement
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

### Functions
```csharp
quint sum(quint a, quint b){
    return a+b;
}
quint z = 1q;
quint y = 3q;
quint c = sum(z, y);
print c;
```

### Search element in Array Type
```csharp
qustring a = "00111111";
if("01" in a){
    print "Element found.";
}
else{
    print "Element not found.";
}
```

## 🏗️ Features to implement
### Branching on quantum functions and/or a mix of quantum and classical operations
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
### Explicit casting
```csharp
quint a = 1q;
qubit b = (qubit)a;
```
### Quantum types comparison
```csharp
quint a = 0q;
qubit b = (qubit)a;
if(a){ //This should throw
}
if(b){ //This should be false
}
if(a > b){ //This and other comparing operators should be implemented for both qubit and quint
}
```

### Handle quantum scope
```csharp

//In this case, we must execute a piece of code in a quantum realm and another piece on a classical CPU before returning to a quantum circuit.
//It's not clear how we should handle this. Should this be transparent to the user? Should we make it more straightforward that a measurement is needed to sum 'input' and 'x'
{
    quint x = 10q;
    if(x > 0){
        string input = classical_read_user_input(); //just an explanatory example for a function that cannot run on a quantum circuit and must run on a classic CPU.
        x += (int)input;
    }
    x = quantum_sqrt(x);
    measure x;
}

//These two blocks can be two different circuits.
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

//These two blocks cannot be two different circuits because they use the same global variable.
//But we can say that we have two custom gates in the circuit,
//So if a custom gate takes nothing as input, it's a new circuit.
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

### Better Functions
```csharp
//This could be implemented as a custom gate of the quantum circuit, but we need to handle the parameters allocation, release and the scope of the variables.
public quint sum(quint a, quint b){
    return a + b;
}
```
