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

# Python Integration Tests for Combine Backend
find_program(PYTHON_EXECUTABLE NAMES python3 python)

if(PYTHON_EXECUTABLE)
    add_test(
        NAME test_combine_fit_backend
        COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_SOURCE_DIR}/python/test_combine_backend.py
    )

    # Ensure test data assets are fully downloaded via CI before running this test
    set_tests_properties(test_combine_fit_backend PROPERTIES DEPENDS get_test_inputs)
endif()
