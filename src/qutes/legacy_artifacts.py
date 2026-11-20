"""Compatibility guard for the published schema-3/4 generated Python template."""
from qutes.serialization import json_text


def guard_binding(metadata, caller):
    # Old templates call validate_metadata(metadata) inside _binding(inputs),
    # before deciding whether to invoke the unversioned compiler import. They
    # cannot pass inputs to a new adapter API. Inspect only that immediate,
    # documented template frame; do not mutate globals or intercept compilation.
    if caller.f_code.co_name != "_binding" or "_METADATA_JSON" not in caller.f_globals:
        return
    inputs = caller.f_locals.get("inputs")
    if inputs is None:
        return
    try:
        same = json_text(inputs) == json_text(metadata["inputs"])
    except (TypeError, ValueError, RecursionError):
        same = False
    if not same:
        raise ValueError("Qutes 0.3 artifacts support cached inputs only under Qutes 0.4; "
                         "array assignment now shares storage. Review array copies and rebuild "
                         "the source with 'qutes build' before changing inputs.")
