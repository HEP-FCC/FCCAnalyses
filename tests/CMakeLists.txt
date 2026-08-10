add_subdirectory(unittest)

add_subdirectory(benchmark)

add_subdirectory(integration)

find_package(Python3 REQUIRED COMPONENTS Interpreter)

add_test(
  NAME grid_submission_python
  COMMAND ${Python3_EXECUTABLE} -m unittest discover
          -s ${CMAKE_CURRENT_LIST_DIR}/python
          -p test_*.py
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
add_test(
  NAME grid_submission_worker_wrapper
  COMMAND ${CMAKE_CURRENT_LIST_DIR}/scripts/test_run_fccanalysis.sh
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
add_test(
  NAME grid_submission_dirac_launcher
  COMMAND ${CMAKE_CURRENT_LIST_DIR}/scripts/test_run_dirac_submission.sh
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

set_tests_properties(
  grid_submission_python
  grid_submission_worker_wrapper
  grid_submission_dirac_launcher
  PROPERTIES LABELS "unit;grid-submission"
)

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
