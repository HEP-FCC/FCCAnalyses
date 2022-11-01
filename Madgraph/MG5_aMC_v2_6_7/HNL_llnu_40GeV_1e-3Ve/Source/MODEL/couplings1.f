ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c      written by the UFO converter
ccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

      SUBROUTINE COUP1()

      IMPLICIT NONE
      INCLUDE 'model_functions.inc'

      DOUBLE PRECISION PI, ZERO
      PARAMETER  (PI=3.141592653589793D0)
      PARAMETER  (ZERO=0D0)
      INCLUDE 'input.inc'
      INCLUDE 'coupl.inc'
      GC_22 = (MDL_EE*MDL_COMPLEXI)/(MDL_SW*MDL_SQRT__2)
      GC_40 = (MDL_EE*MDL_COMPLEXI*MDL_SW)/MDL_CW
      GC_44 = -(MDL_CW*MDL_EE*MDL_COMPLEXI)/(2.000000D+00*MDL_SW)
     $ +(MDL_EE*MDL_COMPLEXI*MDL_SW)/(2.000000D+00*MDL_CW)
      GC_49 = (MDL_EE*MDL_COMPLEXI*MDL_VEN1)/(MDL_SW*MDL_SQRT__2)
      GC_50 = (MDL_EE*MDL_COMPLEXI*MDL_VEN1)/(2.000000D+00*MDL_CW
     $ *MDL_SW)
      GC_52 = -(MDL_EE*MDL_COMPLEXI*MDL_MN1*MDL_VEN1)/(2.000000D+00
     $ *MDL_MW*MDL_SW)
      GC_149 = -((MDL_COMPLEXI*MDL_YE)/MDL_SQRT__2)
      END
