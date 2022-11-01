#ifndef _INCLUDE_FASTJET_CONFIG_AUTO_H
#define _INCLUDE_FASTJET_CONFIG_AUTO_H 1
 
/* include/fastjet/config_auto.h. Generated automatically at end of configure. */
/* include/fastjet/config_raw.h.  Generated from config.h.in by configure.  */
/* config.h.in.  Generated from configure.ac by autoheader.  */

/* The ATLASCone plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_ATLASCONE 
#define FASTJET_ENABLE_PLUGIN_ATLASCONE  /**/ 
#endif

/* The CDFCones plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_CDFCONES 
#define FASTJET_ENABLE_PLUGIN_CDFCONES  /**/ 
#endif

/* The CMSIterativeCone plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE 
#define FASTJET_ENABLE_PLUGIN_CMSITERATIVECONE  /**/ 
#endif

/* The D0RunICone plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_D0RUNICONE 
#define FASTJET_ENABLE_PLUGIN_D0RUNICONE  /**/ 
#endif

/* The D0RunIICone plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_D0RUNIICONE 
#define FASTJET_ENABLE_PLUGIN_D0RUNIICONE  /**/ 
#endif

/* The EECambridge plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_EECAMBRIDGE 
#define FASTJET_ENABLE_PLUGIN_EECAMBRIDGE  /**/ 
#endif

/* The GridJet plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_GRIDJET 
#define FASTJET_ENABLE_PLUGIN_GRIDJET  /**/ 
#endif

/* The Jade plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_JADE 
#define FASTJET_ENABLE_PLUGIN_JADE  /**/ 
#endif

/* The NestedDefs plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_NESTEDDEFS 
#define FASTJET_ENABLE_PLUGIN_NESTEDDEFS  /**/ 
#endif

/* The PxCone plugin is enabled */
/* #undef ENABLE_PLUGIN_PXCONE */

/* The SISCone plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_SISCONE 
#define FASTJET_ENABLE_PLUGIN_SISCONE  /**/ 
#endif

/* The TrackJet plugin is enabled */
#ifndef FASTJET_ENABLE_PLUGIN_TRACKJET 
#define FASTJET_ENABLE_PLUGIN_TRACKJET  /**/ 
#endif

/* compile the deprecated parts of the interface using auto-ptr */
/* #undef HAVE_AUTO_PTR_INTERFACE */

/* compiler supports c++14 deprecated keyword */
/* #undef HAVE_CXX14_DEPRECATED */

/* defined if demangling is enabled at configure time and is supported through
   the GNU C++ ABI */
/* #undef HAVE_DEMANGLING_SUPPORT */

/* Define to 1 if you have the <dlfcn.h> header file. */
#ifndef FASTJET_HAVE_DLFCN_H 
#define FASTJET_HAVE_DLFCN_H  1 
#endif

/* Define to 1 if you have the <execinfo.h> header file. */
#ifndef FASTJET_HAVE_EXECINFO_H 
#define FASTJET_HAVE_EXECINFO_H  1 
#endif

/* compiler supports the "explicit" keyword for operators */
/* #undef HAVE_EXPLICIT_FOR_OPERATORS */

/* Define to 1 if you have the <gmp.h> header file. */
/* #undef HAVE_GMP_H */

/* compiler supports GNU c++ deprecated attribute */
#ifndef FASTJET_HAVE_GNUCXX_DEPRECATED 
#define FASTJET_HAVE_GNUCXX_DEPRECATED  /**/ 
#endif

/* Define to 1 if you have the <inttypes.h> header file. */
#ifndef FASTJET_HAVE_INTTYPES_H 
#define FASTJET_HAVE_INTTYPES_H  1 
#endif

/* Define to 1 if you have the `m' library (-lm). */
#ifndef FASTJET_HAVE_LIBM 
#define FASTJET_HAVE_LIBM  1 
#endif

/* Define to 1 if you have the <memory.h> header file. */
#ifndef FASTJET_HAVE_MEMORY_H 
#define FASTJET_HAVE_MEMORY_H  1 
#endif

/* Define to 1 if you have the <mpfr.h> header file. */
/* #undef HAVE_MPFR_H */

/* compiler supports the "override" keyword */
/* #undef HAVE_OVERRIDE */

/* Define to 1 if you have the <stdint.h> header file. */
#ifndef FASTJET_HAVE_STDINT_H 
#define FASTJET_HAVE_STDINT_H  1 
#endif

/* Define to 1 if you have the <stdlib.h> header file. */
#ifndef FASTJET_HAVE_STDLIB_H 
#define FASTJET_HAVE_STDLIB_H  1 
#endif

/* Define to 1 if you have the <strings.h> header file. */
#ifndef FASTJET_HAVE_STRINGS_H 
#define FASTJET_HAVE_STRINGS_H  1 
#endif

/* Define to 1 if you have the <string.h> header file. */
#ifndef FASTJET_HAVE_STRING_H 
#define FASTJET_HAVE_STRING_H  1 
#endif

/* Define to 1 if you have the <sys/stat.h> header file. */
#ifndef FASTJET_HAVE_SYS_STAT_H 
#define FASTJET_HAVE_SYS_STAT_H  1 
#endif

/* Define to 1 if you have the <sys/types.h> header file. */
#ifndef FASTJET_HAVE_SYS_TYPES_H 
#define FASTJET_HAVE_SYS_TYPES_H  1 
#endif

/* Define to 1 if you have the <unistd.h> header file. */
#ifndef FASTJET_HAVE_UNISTD_H 
#define FASTJET_HAVE_UNISTD_H  1 
#endif

/* Define to the sub-directory where libtool stores uninstalled libraries. */
#ifndef FASTJET_LT_OBJDIR 
#define FASTJET_LT_OBJDIR  ".libs/" 
#endif

/* Name of package */
#ifndef FASTJET_PACKAGE 
#define FASTJET_PACKAGE  "fastjet" 
#endif

/* Define to the address where bug reports for this package should be sent. */
#ifndef FASTJET_PACKAGE_BUGREPORT 
#define FASTJET_PACKAGE_BUGREPORT  "" 
#endif

/* Define to the full name of this package. */
#ifndef FASTJET_PACKAGE_NAME 
#define FASTJET_PACKAGE_NAME  "FastJet" 
#endif

/* Define to the full name and version of this package. */
#ifndef FASTJET_PACKAGE_STRING 
#define FASTJET_PACKAGE_STRING  "FastJet 3.3.4" 
#endif

/* Define to the one symbol short name of this package. */
#ifndef FASTJET_PACKAGE_TARNAME 
#define FASTJET_PACKAGE_TARNAME  "fastjet" 
#endif

/* Define to the home page for this package. */
#ifndef FASTJET_PACKAGE_URL 
#define FASTJET_PACKAGE_URL  "" 
#endif

/* Define to the version of this package. */
#ifndef FASTJET_PACKAGE_VERSION 
#define FASTJET_PACKAGE_VERSION  "3.3.4" 
#endif

/* Define to 1 if you have the ANSI C header files. */
#ifndef FASTJET_STDC_HEADERS 
#define FASTJET_STDC_HEADERS  1 
#endif

/* Version number of package */
#ifndef FASTJET_VERSION 
#define FASTJET_VERSION  "3.3.4" 
#endif

/* Major version of this package */
#ifndef FASTJET_VERSION_MAJOR 
#define FASTJET_VERSION_MAJOR  3 
#endif

/* Minor version of this package */
#ifndef FASTJET_VERSION_MINOR 
#define FASTJET_VERSION_MINOR  3 
#endif

/* Version of the package under the form XYYZZ (instead of X.Y.Z) */
#ifndef FASTJET_VERSION_NUMBER 
#define FASTJET_VERSION_NUMBER  30304 
#endif

/* Patch version of this package */
#ifndef FASTJET_VERSION_PATCHLEVEL 
#define FASTJET_VERSION_PATCHLEVEL  4 
#endif

/* Pre-release version of this package */
/* #undef VERSION_PRERELEASE */
 
/* once: _INCLUDE_FASTJET_CONFIG_AUTO_H */
#endif
