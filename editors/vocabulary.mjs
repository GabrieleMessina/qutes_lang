export default {
  "types": [
    "bool",
    "char",
    "complex",
    "float",
    "int",
    "qubit",
    "quchar",
    "quint",
    "qustring",
    "string",
    "void"
  ],
  "keywords": [
    "else",
    "for",
    "foreach",
    "if",
    "in",
    "input",
    "mut",
    "new",
    "readonly",
    "return",
    "while"
  ],
  "constants": [
    "true",
    "false",
    "pi"
  ],
  "builtins": {
    "superposition": [
      [],
      [
        "values"
      ],
      [
        "values",
        "probabilities: weights"
      ],
      [
        "values",
        "amplitudes: weights"
      ]
    ],
    "measure": [
      [
        "value"
      ]
    ],
    "rotateLeft": [
      [
        "value",
        "amount"
      ]
    ],
    "rotateRight": [
      [
        "value",
        "amount"
      ]
    ],
    "search": [
      [
        "collection",
        "oracle"
      ]
    ],
    "copy": [
      [
        "arrayOrSlice"
      ]
    ],
    "complex": [
      [
        "real",
        "imag"
      ]
    ],
    "hadamard": [
      [
        "mut qubit q"
      ]
    ],
    "not": [
      [
        "mut qubit q"
      ]
    ],
    "phaseFlip": [
      [
        "mut qubit q"
      ]
    ],
    "phase": [
      [
        "mut qubit q",
        "float angle"
      ]
    ],
    "swap": [
      [
        "mut qubit a",
        "mut qubit b"
      ]
    ]
  }
};
