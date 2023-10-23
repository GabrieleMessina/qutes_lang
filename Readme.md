# Qutes Lang
A high level programming language for quantum computing.

## How to Run
### 1. Install python requirements
```bash
pip install -r requirements.txt
```
### 2. Compile the antlr grammar
With [this](https://marketplace.visualstudio.com/items?itemName=mike-lischke.vscode-antlr4) antlr VS Code extension, or:
```bash
antlr4 -Dlanguage=Python3 Qutes.g4
```
### 3. Compile the Qutes source code
```bash
python ./Qutes.py ./GrammarTest.qut
```

### Notes
You can follow the official antlr repository [starting guide for Python](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) if you need a helping hand getting the environment ready.
