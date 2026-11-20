"""PyInstaller one-folder CLI, using the compiler installed from the release commit."""
from importlib.metadata import distribution
from pathlib import Path

from PyInstaller.utils.hooks import collect_data_files, collect_dynamic_libs, collect_submodules, copy_metadata

data = []
binaries = []
hidden = ["matplotlib.backends.backend_agg", "matplotlib.backends.backend_svg"]
for package in ("qiskit", "qiskit_aer"):
    # Qiskit loads synthesis plugins via entry points and styles from package data.
    data.extend(collect_data_files(package))
    binaries.extend(collect_dynamic_libs(package))
    hidden.extend(collect_submodules(package))

# Importable modules and distribution metadata are separate in a frozen bundle.
for dist_name in ("qutes-lang", "antlr4-python3-runtime", "numpy", "qiskit", "qiskit-aer",
                  "stevedore", "matplotlib", "pylatexenc"):
    data.extend(copy_metadata(dist_name))
for entry in distribution("qiskit").entry_points:
    hidden.append(entry.module)

analysis = Analysis([str(Path(SPECPATH) / "launcher.py")], binaries=binaries, datas=data,
                    hiddenimports=hidden, excludes=["IPython", "ipykernel", "pytest", "tkinter"],
                    hooksconfig={"matplotlib": {"backends": ["Agg", "svg"]}})
exe = EXE(PYZ(analysis.pure), analysis.scripts, [], exclude_binaries=True,
          name="qutes", console=True, upx=False)
bundle = COLLECT(exe, analysis.binaries, analysis.datas, name="qutes", upx=False)
