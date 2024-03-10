# Qutes Lang
<!-- A **High Level programming language** for **quantum computing** that allows **everyone**, even those who do not know the theory behind quantum computing in detail, **to exploit its potential** and adapt it to their field of interest -->

<style>
.nano{
    font-size: .5rem;
}
#cool-divider{
/* SVG by SVGBackgrounds.com */
margin: 8px;
padding: 16px;
background-color: #07253677;
background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200' viewBox='0 0 800 800'%3E%3Cg fill='none' stroke='%23169F92' stroke-width='1'%3E%3Cpath d='M769 229L1037 260.9M927 880L731 737 520 660 309 538 40 599 295 764 126.5 879.5 40 599-197 493 102 382-31 229 126.5 79.5-69-63'/%3E%3Cpath d='M-31 229L237 261 390 382 603 493 308.5 537.5 101.5 381.5M370 905L295 764'/%3E%3Cpath d='M520 660L578 842 731 737 840 599 603 493 520 660 295 764 309 538 390 382 539 269 769 229 577.5 41.5 370 105 295 -36 126.5 79.5 237 261 102 382 40 599 -69 737 127 880'/%3E%3Cpath d='M520-140L578.5 42.5 731-63M603 493L539 269 237 261 370 105M902 382L539 269M390 382L102 382'/%3E%3Cpath d='M-222 42L126.5 79.5 370 105 539 269 577.5 41.5 927 80 769 229 902 382 603 493 731 737M295-36L577.5 41.5M578 842L295 764M40-201L127 80M102 382L-261 269'/%3E%3C/g%3E%3Cg fill='%233CFFA7'%3E%3Ccircle cx='769' cy='229' r='6'/%3E%3Ccircle cx='539' cy='269' r='6'/%3E%3Ccircle cx='603' cy='493' r='6'/%3E%3Ccircle cx='731' cy='737' r='6'/%3E%3Ccircle cx='520' cy='660' r='6'/%3E%3Ccircle cx='309' cy='538' r='6'/%3E%3Ccircle cx='295' cy='764' r='6'/%3E%3Ccircle cx='40' cy='599' r='6'/%3E%3Ccircle cx='102' cy='382' r='6'/%3E%3Ccircle cx='127' cy='80' r='6'/%3E%3Ccircle cx='370' cy='105' r='6'/%3E%3Ccircle cx='578' cy='42' r='6'/%3E%3Ccircle cx='237' cy='261' r='6'/%3E%3Ccircle cx='390' cy='382' r='6'/%3E%3C/g%3E%3C/svg%3E");
}
</style>

<div id="cool-divider" style="position: relative;">
<center><h1>Qutes Lang</h1></center>
<center><big>A <b>High Level programming language</b> for <b>quantum computing</b> that allows <b>everyone</b>, even those who do not know the theory behind quantum computing in detail, <b>to exploit its potential</b> and adapt it to their field of interest
</big></center>
<div class="nano" style="position: absolute; bottom:0; right:0;">
<a style="color:#FFF" href="https://www.svgbackgrounds.com/set/free-svg-backgrounds-and-patterns/">SVG by SVGBackgrounds.com</a>
</div>
</div>


## How to Run - 🧭 Easy Start
You can use a GitHub Codespace to start work with Qutes quickly.

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
    int b = 100; //this int b override the upper bool b.  
}
b = true; //this b refer to the bool b.
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
//states we want the qubit is able to take
qubit b = [0, 1]q;
//shorter syntax for a qubit that take only the zero value
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
if(a > b){ //This and other comparing operator should be implemented for both qubit and quint
}
```

### Handle quantum scope
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

### Better Functions
```csharp
//This could be implemented as a custom gate of the quantum circuit, but we need to handle the parameters allocation, release and the scope of the variables.
public quint sum(quint a, quint b){
    return a + b;
}
```