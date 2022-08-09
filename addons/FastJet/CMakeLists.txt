find_package(FastJet REQUIRED)
message(STATUS "includes-------------------------- fastjet: ${FASTJET_INCLUDE_DIRS}")

file(GLOB sources src/*.cc)
file(GLOB headers *.h)

fccanalyses_addon_build(FastJet
                        SOURCES ${sources} ${headers}
                        EXT_HEADERS ${FASTJET_INCLUDE_DIRS}
                        EXT_LIBS ${FASTJET_LIBRARY} ${FASTJET_LIBRARY_DIRS}/libfastjetplugins.so
                        INSTALL_COMPONENT fastjet)
