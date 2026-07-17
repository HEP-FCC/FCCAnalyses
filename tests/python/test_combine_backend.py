#!/usr/bin/env python3
import os
import subprocess
import shutil
import sys

# Dynamically calculate the repository root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

def test_combine_backend_execution():
    """Integration test to verify datacard generation and fit execution."""
    
    # Anchor all relative tracks directly to the dynamic REPO_ROOT
    test_config = os.path.join(REPO_ROOT, "examples", "fcc_ee_zh_mumu_bb.py") 
    test_output_dir = os.path.join(REPO_ROOT, "outputs", "test_integration", "mumu")
    test_datacard = os.path.join(test_output_dir, "datacard.txt")
    
    if not os.path.exists(test_config):
        print(f"----> ERROR: Target config missing at: {test_config}")
        sys.exit(1)
        
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    # Invoke via the explicit 'fccanalysis' executable environment entry point
    command = [
        "fccanalysis", "fit", test_config,
        "-o", test_datacard,
        "-e",
        "--", "-M", "FitDiagnostics"
    ]
    
    print(f"----> Running verification command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"----> ERROR: Framework execution failed!\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
        sys.exit(1)
        
    if not os.path.exists(test_datacard):
        print("----> ERROR: Datacard file asset was not generated successfully!")
        sys.exit(1)

if __name__ == "__main__":
    print("----> INFO: Starting Combine backend integration test...")
    test_combine_backend_execution()
    print("----> INFO: Integration test PASSED successfully!")
    sys.exit(0)
