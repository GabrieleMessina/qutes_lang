def binary(a:int, length:int=None) -> str:
    if length != None:
        return '{0:0{1}b}'.format(a, length)
    else:
        return bin(a).removeprefix('0b')

def is_power_of_two(n):
    return (n != 0) and (n & (n-1) == 0)
    
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