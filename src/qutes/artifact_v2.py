"""Versioned generated-module contract, separate from the source compiler API."""
from qutes.runtime import ResultLayout, checked_build, execute, result_from_data


def validate_metadata(metadata):
    if metadata.get("artifact_schema") != 2 or metadata.get("language_version") != "0.2":
        raise ValueError("unsupported Qutes artifact schema or language version; "
                         "migrate the source and rebuild it with 'qutes build'")


def layout_from_metadata(metadata):
    validate_metadata(metadata)
    return ResultLayout(result_from_data(metadata["result_layout"]), metadata)
