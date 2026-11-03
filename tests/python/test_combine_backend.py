import os
import subprocess
import shutil
import sys

# Dynamically calculate the repository root directory
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))

def test_combine_backend_execution():
    """Integration test to verify datacard generation, fit execution, and result extraction."""
    
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

    # Explicitly preserve and inject local paths into PYTHONPATH for isolated runners
    test_env = os.environ.copy()
    local_python_dir = os.path.join(REPO_ROOT, "python")
    local_bin_dir = os.path.join(REPO_ROOT, "bin")
    current_python_path = test_env.get("PYTHONPATH", "")
    
    if current_python_path:
        test_env["PYTHONPATH"] = f"{local_python_dir}:{local_bin_dir}:{current_python_path}"
    else:
        test_env["PYTHONPATH"] = f"{local_python_dir}:{local_bin_dir}"

    # Test `fccanalysis fit`
    command_fit = [
        sys.executable, local_fccanalysis, "fit", test_config,
        "-o", test_datacard,
        "-e",
        "--", "-M", "FitDiagnostics"
    ]
    
    print(f"----> Running fit verification command: {' '.join(command_fit)}")
    result_fit = subprocess.run(command_fit, capture_output=True, text=True, cwd=REPO_ROOT, env=test_env)
    
    if result_fit.returncode == 6:
        print("----> WARNING: 'combine' tool not found in this environment. Skipping fit & extraction execution test.")
        sys.exit(0)
    elif result_fit.returncode != 0:
        print(f"----> ERROR: Framework fit execution failed!\nSTDOUT:\n{result_fit.stdout}\nSTDERR:\n{result_fit.stderr}")
        sys.exit(1)
        
    if not os.path.exists(test_datacard):
        print("----> ERROR: Datacard file asset was not generated successfully!")
        sys.exit(1)

    print("----> INFO: Datacard generation & fit execution PASSED.")

    # Test `fccanalysis extract`
    command_extract = [
        sys.executable, local_fccanalysis, "extract", test_output_dir
    ]

    print(f"----> Running extraction verification command: {' '.join(command_extract)}")
    result_extract = subprocess.run(command_extract, capture_output=True, text=True, cwd=REPO_ROOT, env=test_env)

    if result_extract.returncode != 0:
        print(f"----> ERROR: Framework extraction execution failed!\nSTDOUT:\n{result_extract.stdout}\nSTDERR:\n{result_extract.stderr}")
        sys.exit(1)

    print("----> INFO: Result extraction PASSED.")

if __name__ == "__main__":
    print("----> INFO: Starting Combine backend integration test suite (fit + extract)...")
    test_combine_backend_execution()
    print("----> INFO: Integration test suite PASSED successfully!")
    sys.exit(0)