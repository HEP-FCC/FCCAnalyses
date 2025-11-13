add_subdirectory(unittest)

add_subdirectory(benchmark)

add_subdirectory(integration)

add_integration_test("examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py")
add_integration_test("examples/FCCee/higgs/mH-recoil/ee/analysis_stage1.py")
add_integration_test("examples/FCCee/flavour/Bc2TauNu/analysis_B2TauNu_truth.py")
add_integration_test("examples/FCCee/test/jet_constituents.py")
add_integration_test("examples/FCCee/vertex_lcfiplus/analysis_V0.py")
add_integration_test("examples/FCCee/weaver/stage1.py")

add_standalone_test("examples/FCCee/fullSim/caloNtupleizer/analysis.py")

add_standalone_test("examples/FCChh/ggHH_bbyy/analysis_stage1.py")

if(WITH_PODIO_DATASOURCE)
  add_standalone_test("examples/data_source/standalone.py")
  add_integration_test("examples/data_source/histmaker_source.py")
  add_integration_test("examples/data_source/stages_source.py")
  add_integration_test("examples/data_source/analysis_stage1.py")
endif()

# TODO: make this test run in the spack build environment
#add_generic_test(build_new_case_study "tests/build_new_case_study.sh")
