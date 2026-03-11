import json

class Submit:
    def __init__(self, submit_dict):
        self.submit_dict = submit_dict
        self.iterable = None
    def set_iterable(self, name, iterable):
        self.iterable = iterable
    def queue(self, txn):
        # Access the simulated schedd logic
        return txn.parent.trigger_logic()
    def __str__(self):
        return json.dumps(self.submit_dict, indent=4)

class Schedd:
    def __init__(self):
        self.attempts = 0
    def transaction(self):
        class MockTxn:
            def __init__(self, parent): self.parent = parent
            def __enter__(self): return self
            def __exit__(self, *args): pass
        return MockTxn(self)
    def trigger_logic(self):
        self.attempts += 1
        if self.attempts < 3:
            raise Exception("Grid Connection Lost")
        return "12345.0"
    def jobs(self, cluster_id):
        return "all"
    def spool(self, jobs):
        pass
