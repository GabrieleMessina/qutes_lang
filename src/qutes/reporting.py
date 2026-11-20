"""Presentation helpers; no printing or changes to execution settings."""


def configuration_warnings(config):
    if "?" not in config.alphabet:
        return []
    return [{"code": "QW0001", "severity": "warning",
             "message": "The alphabet contains '?': it is an encoded character, but acts as a wildcard on the left of matching. Literal wildcard escaping is not supported.",
             "help": "Classical wildcard patterns do not need an alphabet entry. Keep '?' only when you intend to store that marker in quantum data; it does not prepare a superposition."}]


def storage_size(byte_count, exponent):
    """Format statevector estimates without floating-point overflow."""
    units = ("B", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB")
    if byte_count is None:
        return f"2^{exponent - 60} EiB" if exponent >= 60 else f"2^{exponent} B"
    unit = min(max(0, (byte_count.bit_length() - 1) // 10), len(units) - 1)
    scale = 1 << (10 * unit)
    hundredths = (byte_count * 100 + scale // 2) // scale
    whole, fraction = divmod(hundredths, 100)
    value = str(whole) + (f".{fraction:02d}".rstrip("0") if fraction else "")
    return f"{value} {units[unit]}"
