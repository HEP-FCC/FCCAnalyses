
add_subdirectory(unittest)

add_subdirectory(benchmark)


add_integration_test_2("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")

add_integration_test("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")
add_integration_test("examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py")
add_integration_test("examples/FCCee/test/jet_constituents.py")
