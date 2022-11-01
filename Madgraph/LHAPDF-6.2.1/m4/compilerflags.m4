AC_DEFUN([AC_CEDAR_CHECKCXXFLAG], [
  AC_LANG_PUSH(C++)
  AC_MSG_CHECKING([if the $CXX compiler accepts the $1 flag])
  AC_LANG_CONFTEST([AC_LANG_PROGRAM([],[return 0;])])
  flag_ok=no
  stat_string=`$CXX $1 conftest.cpp -o lhapdf-cpp-conf.tmp 2>&1 1>&5` ; test -z "$stat_string" && flag_ok=yes
  rm -f lhapdf-cpp-conf.tmp
  AC_MSG_RESULT([$flag_ok])
  if test x$flag_ok == xyes; then 
    true
    $2
  else
    true
    $3
  fi
  AC_LANG_POP(C++)
])

AC_DEFUN([AC_CEDAR_CHECKFCFLAG], [
  AC_LANG_PUSH(Fortran)
  AC_MSG_CHECKING([if the $FC compiler accepts the $1 flag])
  AC_LANG_CONFTEST([AC_LANG_PROGRAM([],[return])])
  flag_ok=no
  stat_string=`$FC $1 conftest.f -o lhapdf-fc-conf.tmp 2>&1 1>&5` ; test -z "$stat_string" && flag_ok=yes
  rm -f lhapdf-fc-conf.tmp
  AC_MSG_RESULT([$flag_ok])
  if test x$flag_ok == xyes; then 
    true
    $2
  else
    true
    $3
  fi
  AC_LANG_POP(Fortran)
])
