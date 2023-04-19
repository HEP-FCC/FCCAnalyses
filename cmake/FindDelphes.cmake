set(searchpath
  $ENV{DELPHES_DIR}
  $ENV{DELPHES_DIR}/external
  $ENV{DELPHES_DIR}/lib
  $ENV{DELPHES_DIR}/include
  $ENV{DELPHES_DIR}/include/TrackCovariance
#  $ENV{DELPHES}
#  $ENV{DELPHES}/external
#  $ENV{DELPHES}/lib
#  $ENV{DELPHES}/include
  )


find_library(DELPHES_LIBRARY
              NAMES Delphes delphes
              HINTS ${searchpath}
              PATH_SUFFIXES lib)

find_path(DELPHES_INCLUDE_DIR
        #   NAMES DelphesClasses.h Delphes.h
           NAMES classes/DelphesClasses.h modules/Delphes.h external/ExRootAnalysis
           HINTS ${searchpath}
           PATH_SUFFIXES include)

find_path(DELPHES_EXTERNALS_INCLUDE_DIR
             #   NAMES DelphesClasses.h Delphes.h
           NAMES ExRootAnalysis/ExRootConfReader.h
           HINTS ${searchpath}
           PATH_SUFFIXES include
)

find_path(DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR
             #   NAMES DelphesClasses.h Delphes.h
           NAMES TrkUtil.h
           HINTS ${searchpath}
           PATH_SUFFIXES include
)

# Necessary to run the tests
find_path(DELPHES_BINARY_DIR
          NAMES DelphesROOT
          HINTS ${DELPHES_INCLUDE_DIR}/../bin
)

find_path(DELPHES_CARDS_DIR
          NAMES delphes_card_IDEA.tcl
          HINTS ${searchpath}
          PATH_SUFFIXES cards)

unset(searchpath)

set(DELPHES_INCLUDE_DIRS ${DELPHES_INCLUDE_DIR} ${DELPHES_EXTERNALS_INCLUDE_DIR})
set(DELPHES_EXTERNALS_INCLUDE_DIRS ${DELPHES_EXTERNALS_INCLUDE_DIR})
set(DELPHES_EXTERNALS_TKCOV_INCLUDE_DIRS  ${DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR})
set(DELPHES_LIBRARIES ${DELPHES_LIBRARY})

# Delphes does not offer an obvious version indicator, but we need to know
# whether the TrackCovariance module is available or not. So here we simply
# check whether the corresponding header is installed
find_file(DELPHES_TRACK_COV_HEADER modules/TrackCovariance.h PATHS ${DELPHES_INCLUDE_DIRS} NO_DEFAULT_PATHS)

include(FindPackageHandleStandardArgs)
# handle the QUIETLY and REQUIRED arguments and set DELPHES_FOUND to TRUE
# if all listed variables are TRUE
find_package_handle_standard_args(Delphes DEFAULT_MSG DELPHES_INCLUDE_DIR  DELPHES_EXTERNALS_INCLUDE_DIR DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR DELPHES_LIBRARY)

mark_as_advanced(DELPHES_INCLUDE_DIR DELPHES_EXTERNALS_INCLUDE_DIR DELPHES_EXTERNALS_TKCOV_INCLUDE_DIR DELPHES_LIBRARY DELPHES_BINARY_DIR DELPHES_TRACK_COV_HEADER)
