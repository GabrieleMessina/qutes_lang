# Run the local starter

From the extracted release bundle, create and activate a Python 3.12 or 3.13 virtual environment. In its root run `python -m pip install --find-links wheels "qutes-lang[backend]==2.0.0"`. From a source checkout, run `python -m pip install ".[backend]"` instead.

Run `qutes run examples/language/41_bell_gates.qut --shots 64 --seed 17`. To continue an edited browser project, extract its ZIP, change into that directory, and run `qutes run main.qut --config qutes.toml --inputs inputs.json --shots 64 --seed 17`. Run `qutes explain main.qut --config qutes.toml --inputs inputs.json` to see resource use.

Remove a semicolon, run `qutes check main.qut`, and use the location in the error to restore it. Add `not(bob);` before the return in the Bell program to reverse the correlation. Build editable Qiskit Python with `qutes build main.qut --config qutes.toml --inputs inputs.json -o bell.py`.

Download the [standalone Bell starter](https://github.com/GabrieleMessina/qutes_lang/releases/download/2.0.0/qutes-starter.zip) for a ready-to-edit main.qut. To assemble the same starter from the release bundle, run `python resources/starters/build_starter.py dist/qutes-resources-2.0.0.zip dist/qutes-starter.zip` in the source checkout.
