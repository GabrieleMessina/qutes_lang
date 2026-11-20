"""Generated-module contract for phase-bearing search circuits and owned indices."""
from qutes.runtime import ResultLayout, checked_build, execute, result_from_data
from qutes.legacy_artifacts import guard_binding
import sys


def validate_metadata(metadata):
    if metadata.get("artifact_schema") != 3 or metadata.get("language_version") != "0.3":
        raise ValueError("unsupported Qutes artifact schema or language version; "
                         "rebuild the source with 'qutes build'")
    guard_binding(metadata, sys._getframe(1))


def layout_from_metadata(metadata):
    validate_metadata(metadata)
    return ResultLayout(result_from_data(metadata["result_layout"]), metadata)
