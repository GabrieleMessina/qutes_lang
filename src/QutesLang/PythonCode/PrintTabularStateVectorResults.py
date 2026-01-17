def binary(a:int, length:int=None) -> str:
    if length != None:
        return '{0:0{1}b}'.format(a, length)
    else:
        return bin(a).removeprefix('0b')
    
def int_to_twos_comp(val, n_bits):
    """
    Converts an integer to its two's complement binary string representation with a specified number of bits.
    Args:
        val: The integer value to convert.
        n_bits: The number of bits for the two's complement representation.
    """
    if val < 0:
        val = (1 << n_bits) + val
    format_string = '{0:0' + str(n_bits) + 'b}'
    return format_string.format(val)

def twos_comp_to_int(bin_str):
    """
    Converts a binary string in two's complement to its integer representation.
    Args:
        bin_str: The binary string (e.g., '1101' for -3 in 4 bits)
    """
    n_bits = len(bin_str)
    unsigned_val = int(bin_str, 2)
    
    # Check if the sign bit is set (i.e., if the number is negative)
    if (unsigned_val & (1 << (n_bits - 1))) != 0:
        # Compute the negative value
        return unsigned_val - (1 << n_bits)
    else:
        return unsigned_val

def get_counts_by_register(result) -> dict[str, dict[str, int]]:
    # {reg_name: {bitstring: count}}
    cnt:dict[dict[int]] = {}
    for i, pub_res in enumerate(result): # For each circuit
        for reg_name in pub_res.data:
            reg_name = f'{reg_name}' if i == 0 else f'{reg_name}_circ_{i}'
            cnt[reg_name] = getattr(pub_res.data,reg_name).get_counts()
    return cnt

def get_counts_by_run(result) -> dict[str, int]:
    # {bitstring: count}
    return result[0].join_data().get_counts()

def print_result_table(result, varname_to_register_size, clreg_name_to_actual_name):
    from qiskit import QiskitError
    counts_by_run = {}
    counts_by_registers = {}
    try:
        counts_by_run = get_counts_by_run(result)
        counts_by_registers = get_counts_by_register(result)
    except (QiskitError, ValueError):
        pass

    from tabulate import tabulate
    table = []
    for index, (result, count) in enumerate(counts_by_run.items()):
        i = 0
        while i < len(result):
            row = []
            for reg_name in list(counts_by_registers.keys())[::-1]:
                # reverse the regs list to match the qiskit ordering,
                # measured variables from right to left based on measuring time
                reg_size = varname_to_register_size[reg_name]
                bitstring = result[i:i+reg_size]
                int_value = twos_comp_to_int(bitstring)
                row.append(f"{bitstring}₂ | {int_value}⏨")
                i += reg_size
            row = row[::-1] # recover ordering to have first measured as first column
            row.append(count)
            row.append("Least Significant bit as rightmost") if(index == 0) else row.append("")
            table.append(row)

    if len(table) == 0:
        print("⚠️  ~ No results to show")
        return

    print("⚠️  ~ Following results only show the last execution of the circuit, in case of measurements in the middle of the circuit, like the ones needed for casts and Grover search, those results are not shown.")
    headers = [f"{clreg_name_to_actual_name[reg_name]}" for reg_name in counts_by_registers.keys()]
    headers.append("Counts")
    headers.append("Notes")
    maxcolwidths = [40] * len(headers)
    maxcolwidths[-1] = 40
    colalign = ["right"] * len(headers)
    colalign[-1] = "left"
    print(tabulate(table, headers=headers, stralign="right", tablefmt="fancy_grid", maxcolwidths=maxcolwidths, colalign=colalign))