import sys
import os

# Set up paths so Python can find both the mock and the 'python' package
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("python"))
sys.path.append(os.path.abspath("tests/unit/batch"))

# Pre-emptively mock htcondor
import mock_htcondor
sys.modules['htcondor'] = mock_htcondor

# Now import the actual code
from python.batch import submit_job
import mock_htcondor as htcondor

def test_robustness():
    print("--- Testing Robust Submission (Simulating 2 failures) ---")
    mock_sub = htcondor.Submit({"executable": "test.sh"})
    
    # Run the submission logic
    success = submit_job(mock_sub, spool=False, max_trials=5)
    
    if success:
        print("\nFINAL STATUS: PASS - Code recovered from simulated grid failures.")
    else:
        print("\nFINAL STATUS: FAIL - Logic did not recover.")
        sys.exit(1)

if __name__ == "__main__":
    test_robustness()
