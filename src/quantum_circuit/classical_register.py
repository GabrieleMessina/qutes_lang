from qiskit import ClassicalRegister as cr

class ClassicalRegister(cr):
    def __init__(self, size:int, name:str):
        super().__init__(size, name)
        if not name.replace('_', '').isalnum():
            raise RuntimeError(f"Classical register names must be valid identifiers, but '{var_name}' is not. Valid identifiers contain only alphanumeric letters (a-z and A-Z), decimal digits (0-9), or underscores (_).")
        self.measured_values = []
        self.measured_counts = []