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
antrl4 -Dlanguage=Python3 -message-format antlr -o ./src/qutes_antlr -listener -visitor -Xexact-output-dir ./specification/grammar/qutes_lexer.g4

antrl4 -Dlanguage=Python3 -message-format antlr -o ./src/qutes_antlr -listener -visitor -Xexact-output-dir ./specification/grammar/qutes_parser.g4
```
### 3. Compile the Qutes source code
```bash
python ./src/qutes.py ./specification/grammar/grammar_test.qut
```

### Notes
You can follow the official antlr repository [starting guide for Python](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) if you need a helping hand getting the environment ready.
