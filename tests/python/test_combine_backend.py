import os
import subprocess
import shutil
import pytest

def test_combine_backend_execution():
    """Integration test to verify datacard generation and fit execution."""
    # 1. Setup paths
    test_config = "examples/fcc_ee_zh_mumu_bb.py"
    test_output_dir = "outputs/test_integration/mumu"
    test_datacard = os.path.join(test_output_dir, "datacard.txt")
    
    # Ensure a clean slate for the test
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    # 2. Build the command string
    command = [
        "fccanalysis", "fit", test_config,
        "-o", test_datacard,
        "-e",
        "--", "-M", "FitDiagnostics"
    ]
    
    # 3. Execute the toolchain
    result = subprocess.run(command, capture_output=True, text=True)
    
    # 4. Assertions
    assert result.returncode == 0, f"Framework crashed with error: {result.stderr}"
    assert os.path.exists(test_datacard), "Datacard text file was not generated."
    assert os.path.exists(os.path.join(test_output_dir, "fitDiagnosticsTest.root")), "Combine ROOT output artifact is missing."
    
    # 5. Clean up test outputs
    shutil.rmtree("outputs/test_integration")

if __name__ == "__main__":
    import sys
    print("----> INFO: Starting Combine backend integration test...")
    try:
        test_combine_backend_execution()
        print("----> INFO: Integration test PASSED successfully!")
        sys.exit(0)
    except AssertionError as e:
        print(f"----> ERROR: Integration test FAILED assertion!\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"----> ERROR: Runtime crash during test execution!\n{e}")
        sys.exit(1)
