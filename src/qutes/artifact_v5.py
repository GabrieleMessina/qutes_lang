"""Qutes 0.4 generated-module contract: reference arrays and explicit preparation."""
from qutes.runtime import ResultLayout, checked_build, execute, result_from_data


def validate_metadata(metadata):
    if metadata.get("artifact_schema") != 5 or metadata.get("language_version") != "0.4":
        raise ValueError("unsupported Qutes artifact schema or language version; "
                         "rebuild the source with 'qutes build'")


def layout_from_metadata(metadata):
    validate_metadata(metadata)
    return ResultLayout(result_from_data(metadata["result_layout"]), metadata)
