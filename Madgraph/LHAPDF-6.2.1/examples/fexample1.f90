program example1
  implicit double precision (a-h,o-z)
  character name*64
  double precision f(-6:6)
  character*20 lparm
  logical has_photon
  Dimension Z(10), XX(10)
  Data (Z(I), I=1,10) /.05, .1, .2, .3, .4, .5, .6, .7, .8, .9/

  Do I = 1, 10
     XX(I) = Z(I) **3
  EndDo

   name='cteq6.LHgrid'
  ! name='cteq65.LHgrid'
  ! name='cteq66.LHgrid'
  ! name='MRST2006nnlo.LHgrid'
  ! name='MRST2001E.LHgrid'
  ! name='H12000ms.LHgrid'
  call InitPDFsetByName(name)

  QMZ=91.18d0
  write(*,*)
  call numberPDF(N)
  print *,'There are ',N,' PDF sets'
  do i=0,N
     write(*,*) '---------------------------------------------'
     call InitPDF(i)
     write(*,*) 'PDF set ',i
     call GetXmin(i,xmin)
     call GetXmax(i,xmax)
     call GetQ2min(i,q2min)
     call GetQ2max(i,q2max)
     print *,'xmin=',xmin,' xmax=',xmax,' Q2min=',q2min,' Q2max=',q2max
     call GetMinMax(i,xmin,xmax,q2min,q2max)
     print *,'xmin=',xmin,' xmax=',xmax,' Q2min=',q2min,' Q2max=',q2max
     call setlhaparm('EXTRAPOLATE') !< These work, but have no effect
     call getlhaparm(18,lparm) !< These work, but have no effect
     print *,'lhaparm(18)=',lparm
     write(*,*)
     a=alphasPDF(QMZ)
     write(*,*) 'alpha_S(M_Z) = ',a
     call getLam4M(1,i,xlam4)
     call getLam5M(1,i,xlam5)
     print *,' lambda5: ',xlam5, ' lambda4: ',xlam4
     write(*,*)
     write(*,*) 'x*up'
     write(*,*) '   x     Q=10 GeV     Q=100 GeV    Q=1000 GeV'
     ! q2 = 10.0d0
     ! q = dsqrt(q2)
     q = 50.0d0
     print *,q
     do ix=1,10
        ! x = (ix-0.5d0)/10.0d0
        x = xx(ix)
        ! x = z(ix)
        if(has_photon()) then
          print *,"This set has a photon"
          call evolvePDFphoton(x,Q,f,photon)
        else
          call evolvePDF(x,Q,f)
        endif
        g = f(0)
        u = f(2)
        d = f(1)
        s = f(3)
        c = f(4)
        b = f(5)
        ubar = f(-2)
        dbar = f(-1)
        sbar = f(-3)
        cbar = f(-4)
        bbar = f(-5)
        write(*,'(F7.4,13(1pE10.3))') x,u,d,ubar,Dbar,s,sbar,c,cbar,b,bbar,g,photon
     enddo
  enddo

end program example1
