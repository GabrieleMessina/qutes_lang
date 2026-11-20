"""Export one input-specialized Qiskit circuit and its Qutes return expression."""

from inspect import getsource

from qutes.codegen import circuit_lines
from qutes.serialization import integer_text, json_text


def _signed(bits, width):
    sign = 1 << (width - 1)
    return (bits ^ sign) - sign


def _text(bits, alphabet, length, capacity):
    width = (len(alphabet) - 1).bit_length()
    mask = (1 << width) - 1
    codes = [(bits >> (i * width)) & mask for i in range(capacity)]
    if any(code >= len(alphabet) for code in codes) or any(codes[length:]):
        raise ValueError("Invalid encoded string or nonzero padding")
    return "".join(alphabet[code] for code in codes[:length])


def _literal(value, helpers):
    if isinstance(value, (tuple, list)):
        return "[" + ", ".join(_literal(item, helpers) for item in value) + "]"
    if type(value) is int and value.bit_length() > 2048:
        # Hex literals also work beyond Python's decimal conversion limit.
        helpers.update((integer_text, json_text))
        return hex(value)
    if isinstance(value, complex):
        helpers.update((integer_text, json_text))
    return ascii(value)


def _result_expression(result, args, helpers):
    if result.op == "literal":
        return _literal(result.value, helpers)
    if result.op == "snapshot":
        bits = result.bits
        if result.type.name == "bool":
            return f"bool((memory >> {bits[0]}) & 1)"
        width = len(bits)
        if bits and bits == tuple(range(bits[0], bits[0] + width)):
            packed = f"((memory >> {bits[0]}) & {(1 << width) - 1:#x})"
        else:
            packed = f"sum(((memory >> bit) & 1) << i for i, bit in enumerate({bits!r}))"
        if result.type.name == "int":
            helpers.add(_signed)
            return f"_signed({packed}, {width})"
        alphabet = ascii(result.alphabet)
        if result.type.name == "char":
            return f"{alphabet}[{packed}]"
        if result.type.name == "string":
            helpers.add(_text)
            return f"_text({packed}, {alphabet}, {result.length}, {result.capacity})"
    if result.op == "array":
        return "[" + ", ".join(args) + "]"
    if result.op == "index":
        return f"({args[0]})[{args[1]}]"
    if result.op == "unary:!":
        return f"(not {args[0]})"
    if result.op.startswith("binary:"):
        operator = result.op.removeprefix("binary:")
        operator = {"&&": "and", "||": "or"}.get(operator, operator)
        if operator in ("==", "!=", "<", "<=", ">", ">=", "and", "or"):
            return f"({args[0]} {operator} {args[1]})"
    raise ValueError(f"Unsupported standalone return expression {result.op!r}")


def _decoder_lines(result, helpers):
    lines = ["def decode_result(memory):",
             '    """Decode classical bits in the order of the Qutes return expression."""']
    pending = [(result, False)]
    values = []
    while pending:
        node, ready = pending.pop()
        if node.arguments and not ready:
            pending.append((node, True))
            pending.extend((child, False) for child in reversed(node.arguments))
            continue
        count = len(node.arguments)
        args = values[-count:] if count else []
        if count:
            del values[-count:]
        expression = _result_expression(node, args, helpers)
        if node is result:
            lines.append(f"    return {expression}")
        elif count:
            # Unrolled Qutes loops can exceed Python's nested-expression limit.
            name = f"value_{len(lines) - 1}"
            lines.append(f"    {name} = {expression}")
            values.append(name)
        else:
            values.append(expression)
    return lines


def standalone_source(compilation, *, default_shots=64):
    """Generate a directly runnable file for the already-compiled input binding."""
    program = compilation.program
    if type(default_shots) is not int or not 1 <= default_shots <= program.config.max_simulation_shots:
        raise ValueError("Invalid default shot count")
    helpers = set()
    decoder = _decoder_lines(program.result, helpers)
    lines = [
        '"""Qiskit circuit exported from the Qutes playground.',
        "",
        "Install: python -m pip install qiskit==2.3.0 qiskit-aer==0.17.2",
        f"Run: python experiment.qiskit.py --shots {default_shots} --seed 17",
        "Change construction-time inputs in the playground and export again.",
        '"""',
        f"# Compiled inputs: {json_text(compilation.metadata['inputs'])}",
        "import json", "", "",
    ]
    lines.extend(circuit_lines(program, "build_circuit"))
    for helper in (_signed, _text, integer_text, json_text):
        if helper in helpers:
            lines.extend([getsource(helper).rstrip(), "", ""])
    lines.extend(decoder)
    lines.extend(["", ""])
    serialize = "json_text" if json_text in helpers else "json.dumps"
    lines.append(f'''def run(shots={default_shots}, seed=None):
    """Simulate the circuit and group shots by their decoded return values."""
    if type(shots) is not int or not 1 <= shots <= {program.config.max_simulation_shots}:
        raise ValueError("shots must be in 1..{program.config.max_simulation_shots}")
    if seed is not None and (type(seed) is not int or not 0 <= seed < 2**32):
        raise ValueError("seed must be an unsigned 32-bit integer")
    circuit = build_circuit()
    if circuit.num_clbits:
        from qiskit import transpile
        from qiskit_aer import AerSimulator
        simulator = AerSimulator(method="statevector", max_parallel_threads=1)
        compiled = transpile(circuit, simulator, optimization_level=0, seed_transpiler=seed)
        if compiled.num_qubits > {program.config.max_simulation_qubits}:
            raise ValueError("Circuit exceeds the simulation limit of {program.config.max_simulation_qubits} qubits")
        result = simulator.run(compiled, shots=shots, seed_simulator=seed).result()
        if not result.success:
            raise RuntimeError(result.status)
        counts = result.get_counts().int_outcomes()
    else:
        counts = {{0: shots}}

    outcomes = {{}}
    for memory, count in counts.items():
        value = decode_result(memory)
        key = {serialize}(value)
        row = outcomes.setdefault(key, {{"value": value, "count": 0}})
        row["count"] += count
    rows = [outcomes[key] for key in sorted(outcomes)]
    for row in rows:
        row["probability"] = row["count"] / shots
    return {{"outcomes": rows}}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--shots", type=int, default={default_shots})
    parser.add_argument("--seed", type=int)
    options = parser.parse_args()
    print({serialize}(run(shots=options.shots, seed=options.seed)))
''')
    return "\n".join(lines)
