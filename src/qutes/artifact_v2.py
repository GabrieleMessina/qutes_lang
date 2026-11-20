"""Fail before an older generated module can execute or recompile its source."""
raise ImportError("Qutes 0.2 generated modules require a rebuild for Qutes 0.3. "
                  "Run 'qutes build SOURCE.qut' to regenerate the module.")
