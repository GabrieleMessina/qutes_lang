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

def print_pretty_results_mapped(result, var_names: list, var_sizes: dict, var_to_reg: dict):
    """
    Parses V2 results using specific register mappings and slices them into table columns.
    
    Args:
        result: The PrimitiveResult object.
        var_names: List of strings defining the column order.
        var_sizes: Dict defining how many bits each variable takes (e.g. {'a': 2}).
        var_to_reg: Dict mapping variable names to classical register names (e.g. {'a': 'meas'}).
    """
    from collections import Counter
    from tabulate import tabulate # pyright: ignore[reportMissingModuleSource]
    pub_result = result[0] # Get first experiment data
    data_bin = pub_result.data
    
    # 1. Cache the bitstrings for every register involved
    #    We extract the full list of shots (e.g., 1024 strings) for each register once.
    reg_cache = {}
    unique_regs = set(var_to_reg.values())
    
    for reg in unique_regs:
        try:
            bit_array = getattr(data_bin, reg)
            # get_bitstrings() returns a list of strings, one for each shot e.g. ['101', '000', ...]
            reg_cache[reg] = bit_array.get_bitstrings()
        except AttributeError:
            print(f"Error: Register '{reg}' not found in result data.")
            return

    # 2. Track our position (cursor) within each register 
    #    This allows us to slice if multiple variables share one register.
    #    Assumption: Variables are processed Left-to-Right as they appear in the bitstring.
    reg_cursors = {reg: 0 for reg in unique_regs}
    
    columns = []

    # 3. Build columns
    for var in var_names:
        reg_name = var_to_reg[var]
        num_bits = var_sizes[var]
        
        start_idx = reg_cursors[reg_name]
        end_idx = start_idx + num_bits
        
        # Extract this slice for ALL shots at once (List Comprehension)
        # We assume the user defined var_names in the order they appear in the register string.
        full_strings = reg_cache[reg_name]
        column_data = [s[start_idx : end_idx] for s in full_strings]
        columns.append(column_data)        
        # Update cursor for this register
        reg_cursors[reg_name] = end_idx

    # 4. Transpose columns to rows (reconstruct individual shots)
    #    zip(*columns) turns [[col1_shot1, ...], [col2_shot1, ...]] into [(col1_shot1, col2_shot1), ...]
    rows = list(zip(*columns))
    # rows.append("Least Significant bit as rightmost")
    
    # 5. Count frequencies
    #    We count the unique tuples (rows) representing the outcome of a single shot across all vars.
    counts = Counter(rows)
    
    # 6. Format for Table
    table_data = []
    for row_tuple, count in counts.items():
        formatted_row = [f"{bin_str}₂ | {twos_comp_to_int(bin_str)}⏨" for bin_str in row_tuple]
        formatted_row.append(count)
        table_data.append(formatted_row)

    # 7. Sort and Print
    table_data.sort(key=lambda x: x[-1], reverse=True)
    headers = var_names + ["Count", "Notes"]

    # 8. Add "Notes" column (Only populate first row)
    for i in range(len(table_data)):
        if i == 0:
            table_data[i].append("Least Significant bit as rightmost")
        else:
            table_data[i].append("")

    print("⚠️  ~ Following results only show the last execution of the circuit, in case of measurements in the middle of the circuit, like the ones needed for casts and Grover search, those results are not shown.")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))