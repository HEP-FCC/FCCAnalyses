import sys
import os
from unittest.mock import MagicMock

# Setup paths
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("python"))
sys.path.append(os.path.abspath("tests/unit/batch"))

# The "Black Hole" Mock: If it's a heavy dependency, we kill it here.
# This prevents ModuleNotFoundError for anything batch.py might import.
for module in ['htcondor', 'ROOT', 'yaml', 'cppyy', 'process']:
    sys.modules[module] = MagicMock()

# Manually point 'htcondor' to our mock_htcondor file so the logic actually runs
import mock_htcondor
sys.modules['htcondor'] = mock_htcondor

# Mock the process functions that batch.py expects
mock_process = sys.modules['process']
mock_process.get_process_info = MagicMock(return_value=([], []))
mock_process.get_subfile_list = MagicMock(return_value=[])
mock_process.get_chunk_list = MagicMock(return_value=[])

# Now import the actual logic
from python.batch import submit_job
import mock_htcondor as htcondor

def test_robustness():
    print("--- Testing Robust Submission (Simulating 2 failures) ---")
    # Using Any because we mocked the type hints in batch.py
    mock_sub = htcondor.Submit({"executable": "test.sh"})
    
    success = submit_job(mock_sub, spool=False, max_trials=5)
    
    if success:
        print("\nFINAL STATUS: PASS - Code recovered from simulated grid failures.")
    else:
        print("\nFINAL STATUS: FAIL - Logic did not recover.")
        sys.exit(1)

if __name__ == "__main__":
    test_robustness()
