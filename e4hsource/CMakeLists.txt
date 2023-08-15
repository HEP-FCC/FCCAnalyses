add_library(e4hsource SHARED src/EDM4hepDataSource.cxx)
target_include_directories(e4hsource PUBLIC include)
target_link_libraries(e4hsource PUBLIC ROOT::RIO
                                       ROOT::ROOTDataFrame
                                       podio::podioRootIO
                                       EDM4HEP::edm4hep
                                       EDM4HEP::edm4hepDict
)

ROOT_GENERATE_DICTIONARY(G__FCCAnalyses_EDM4hepDataSource
                         include/EDM4hepDataSource/EDM4hepDataSource.hxx
                         MODULE e4hsource
                         LINKDEF include/EDM4hepDataSource/LinkDef.h
)

install(TARGETS e4hsource
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(FILES "${PROJECT_BINARY_DIR}/e4hsource/libe4hsource.rootmap"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)

install(FILES "${PROJECT_BINARY_DIR}/e4hsource/libe4hsource_rdict.pcm"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)


# Legacy
add_library(e4hlegacysource SHARED src/EDM4hepLegacySource.cxx)
target_include_directories(e4hlegacysource PUBLIC include)
target_link_libraries(e4hlegacysource PUBLIC ROOT::RIO
                                             ROOT::ROOTDataFrame
                                             podio::podioRootIO
                                             EDM4HEP::edm4hep
                                             EDM4HEP::edm4hepDict
)

ROOT_GENERATE_DICTIONARY(G__FCCAnalyses_EDM4hepLegacySource
                         include/EDM4hepDataSource/EDM4hepLegacySource.hxx
                         MODULE e4hlegacysource
                         LINKDEF include/EDM4hepDataSource/Legacy_LinkDef.h
)

install(TARGETS e4hlegacysource
        LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
        PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

install(FILES "${PROJECT_BINARY_DIR}/e4hsource/libe4hlegacysource.rootmap"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)

install(FILES "${PROJECT_BINARY_DIR}/e4hsource/libe4hlegacysource_rdict.pcm"
        DESTINATION "${CMAKE_INSTALL_LIBDIR}"
)
