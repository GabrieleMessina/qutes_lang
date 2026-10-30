"""Run the checkout's developer CLI without installing it globally."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from qutes.cli import main

raise SystemExit(main())
