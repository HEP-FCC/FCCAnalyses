# Low level EDM4hep access
add_executable(integration_low_level_edm4hep
               ${CMAKE_SOURCE_DIR}/tests/integration/low_level_edm4hep.cxx
)
target_link_libraries(integration_low_level_edm4hep ROOT::ROOTDataFrame
                                                    podio::podioDataSource
                                                    EDM4HEP::edm4hep
                                                    EDM4HEP::edm4hepDict
)
add_generic_test(
  integration_low_level_edm4hep
  "${CMAKE_CURRENT_BINARY_DIR}/integration_low_level_edm4hep 1"
  "https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/p8_ee_WW_ecm240_edm4hep.root"
)

add_executable(
  integration_low_level_associations
  ${CMAKE_SOURCE_DIR}/tests/integration/low_level_associations.cxx)
target_link_libraries(integration_low_level_associations ROOT::ROOTDataFrame
                                                         podio::podioDataSource
                                                         EDM4HEP::edm4hep
                                                         EDM4HEP::edm4hepDict
                                                         FCCAnalyses
)
add_generic_test(
  integration_low_level_associations
  "${CMAKE_CURRENT_BINARY_DIR}/integration_low_level_associations 1"
  "https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/p8_ee_WW_ecm240_edm4hep.root"
)

if(WITH_PODIO_DATASOURCE)
  add_executable(integration_data_source
                 ${CMAKE_SOURCE_DIR}/tests/integration/data_source.cxx)
  target_include_directories(integration_data_source PRIVATE ${CMAKE_SOURCE_DIR}/include)
  target_link_libraries(integration_data_source podio::podioDataSource
                                                EDM4HEP::edm4hep
  )
  add_generic_test(
    integration_data_source
    "${CMAKE_CURRENT_BINARY_DIR}/integration_data_source 1"
    "https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/p8_ee_WW_ecm240_edm4hep.root"
  )

  add_executable(
    integration_data_source_associations
    ${CMAKE_SOURCE_DIR}/tests/integration/data_source_associations.cxx
  )
  target_include_directories(integration_data_source_associations PRIVATE
                             ${CMAKE_SOURCE_DIR}/include)
  target_link_libraries(integration_data_source_associations podio::podioDataSource
                                                             EDM4HEP::edm4hep
                                                             FCCAnalyses
  )
  add_generic_test(
    integration_data_source_associations
    "${CMAKE_CURRENT_BINARY_DIR}/integration_data_source_associations 1"
    "https://fccsw.web.cern.ch/fccsw/testsamples/edm4hep1/p8_ee_WW_ecm240_edm4hep.root"
  )
endif()
