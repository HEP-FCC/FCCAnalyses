
add_subdirectory(unittest)

add_test(NAME examples/FCCee/higgs/mH-recoil/mumu
        COMMAND python config/FCCAnalysisRun.py examples/FCCee/higgs/mH-recoil/mumu/analysis_stage1.py --output myoutput.root --files-list root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_131527278.root
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
