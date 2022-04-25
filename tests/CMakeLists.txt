
add_subdirectory(unittest)

add_test(NAME examples/flavor/generic-analysis
        # TODO: check if possible to make eos world readable
        #COMMAND python examples/FCCee/flavour/generic-analysis/analysis.py root://eospublic.cern.ch//eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_131527278.root
        COMMAND python examples/FCCee/flavour/generic-analysis/analysis.py https://fccsw.web.cern.ch/testsamples/fccanalyses/eos/experiment/fcc/ee/generation/DelphesEvents/spring2021/IDEA/p8_ee_Zbb_ecm91_EvtGen_Bc2TauNuTAUHADNU/events_131527278.root
        WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)
