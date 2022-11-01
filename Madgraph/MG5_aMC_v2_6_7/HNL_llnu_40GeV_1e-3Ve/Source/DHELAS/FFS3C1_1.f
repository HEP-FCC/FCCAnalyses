C     This File is Automatically generated by ALOHA 
C     The process calculated in this file is: 
C     (ProjM(2,1)) * C(51,2) * C(52,1)
C     
      SUBROUTINE FFS3C1_1(F1, S3, COUP, M2, W2,F2)
      IMPLICIT NONE
      COMPLEX*16 CI
      PARAMETER (CI=(0D0,1D0))
      COMPLEX*16 F2(6)
      COMPLEX*16 S3(*)
      REAL*8 P2(0:3)
      REAL*8 W2
      COMPLEX*16 F1(*)
      REAL*8 M2
      COMPLEX*16 DENOM
      COMPLEX*16 COUP
      F2(1) = +F1(1)+S3(1)
      F2(2) = +F1(2)+S3(2)
      P2(0) = -DBLE(F2(1))
      P2(1) = -DBLE(F2(2))
      P2(2) = -DIMAG(F2(2))
      P2(3) = -DIMAG(F2(1))
      DENOM = COUP/(P2(0)**2-P2(1)**2-P2(2)**2-P2(3)**2 - M2 * (M2 -CI
     $ * W2))
      F2(3)= DENOM*CI * F1(3)*M2*S3(3)
      F2(4)= DENOM*CI * F1(4)*M2*S3(3)
      F2(5)= DENOM*CI * S3(3)*(F1(3)*(P2(3)-P2(0))+F1(4)*(P2(1)+CI
     $ *(P2(2))))
      F2(6)= DENOM*(-CI )* S3(3)*(F1(3)*(+CI*(P2(2))-P2(1))+F1(4)
     $ *(P2(0)+P2(3)))
      END


