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
    tmp_root = os.environ.get("TMPDIR") or os.environ.get("TEMP") or "/tmp"
    test_output_dir = os.path.join(tmp_root, f"fccanalyses_test_integration_mumu_{os.getpid()}")
    test_datacard = os.path.join(test_output_dir, "datacard.txt")

    if not os.path.exists(test_config):
        print(f"----> ERROR: Target config missing at: {test_config}")
        sys.exit(1)
        
    if os.path.exists(test_output_dir):
        shutil.rmtree(test_output_dir)

    # Target the local script asset directly to avoid pulling the global CVMFS version
    local_fccanalysis = os.path.join(REPO_ROOT, "bin", "fccanalysis")

    # RESTORED: Use sys.executable to perfectly match the active environment's interpreter
    command = [
        sys.executable, local_fccanalysis, "fit", test_config,
        "-o", test_datacard,
        "-e",
        "--", "-M", "FitDiagnostics"
    ]
    
    # Explicitly preserve and inject local paths into PYTHONPATH for isolated runners
    test_env = os.environ.copy()
    local_python_dir = os.path.join(REPO_ROOT, "python")
    local_bin_dir = os.path.join(REPO_ROOT, "bin")
    current_python_path = test_env.get("PYTHONPATH", "")
    
    if current_python_path:
        test_env["PYTHONPATH"] = f"{local_python_dir}:{local_bin_dir}:{current_python_path}"
    else:
        test_env["PYTHONPATH"] = f"{local_python_dir}:{local_bin_dir}"
    
    print(f"----> Running verification command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True, cwd=REPO_ROOT, env=test_env)
    
    if result.returncode == 6:
        print("----> WARNING: 'combine' tool not found in this environment. Skipping execution test.")
    elif result.returncode != 0:
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
