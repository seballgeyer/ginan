MODULE m_eop_igu


! ----------------------------------------------------------------------
! MODULE: m_eop_igu.f03
! ----------------------------------------------------------------------
! Purpose:
!  Module for calling the modified eop_igu subroutine 
! 
! ----------------------------------------------------------------------
! Author :	Dr. Thomas Papanikolaou, Geoscience Australia 
! Created:	28 August 2018
! ----------------------------------------------------------------------


      IMPLICIT NONE
      !SAVE 			
 
	  
Contains

SUBROUTINE eop_igu (mjd, ERP_fname, EOP_days, EOP_int)


! ----------------------------------------------------------------------
! Subroutine:  eop_igu.f90
! ----------------------------------------------------------------------
! Purpose:
!  EOP data reading and processing by using:
!  - ERP (Earth Rotation Parameters) data from the ultra-rapid products 
!    provided by the IGS (International GNSS Service).
!  - Corrections to the precession-nutation model are obtained from the 
!    daily solutions (finals2000A.daily) provided by the International 
!    Earth Rotation Service and Reference Systems (IERS) 
!    Rapid Service/Prediction Center (RS/PC) 
! ----------------------------------------------------------------------
! Input arguments:
! - mjd:			Modified Julian Day number at the required epoch
!					(including fraction of the day)
! - ERP_fname:		IGS ultra-rapid ERP data file name e.g. igu18861_00.erp
! - EOP_days:		EOP data array of the days (data points aplied for interpolation) based on IERS RS/PC EOP data
!
! Output arguments:
! - eop_int:		EOP data array at the input epoch
!   				eop_int = [MJD xp yp UT1_UTC LOD dX dY] 
!   				MJD:     MJD at the input epoch (including fraction of the day)
!   				x,y:     Polar motion coordinates (arcsec) 
!   				UT1_UTC: Difference between UT1 and UTC (sec)
!					dX,dY:   Corrections to Precession-Nutation model (arcsec)
! ----------------------------------------------------------------------
! Dr. Thomas Papanikolaou, Geoscience Australia               March 2016
! ----------------------------------------------------------------------


      USE mdl_precision
      USE mdl_num
      use pod_yaml
      IMPLICIT NONE

! ----------------------------------------------------------------------
! Dummy arguments declaration
! ----------------------------------------------------------------------
! IN
      REAL (KIND = prec_d), INTENT(IN) :: mjd
      CHARACTER (LEN=512), INTENT(IN) :: ERP_fname
      REAL (KIND = prec_d), INTENT(IN), DIMENSION(:,:), ALLOCATABLE :: EOP_days
! OUT
      REAL (KIND = prec_d), INTENT(OUT) :: EOP_int(EOP_MAX_ARRAY)
! ----------------------------------------------------------------------

! ----------------------------------------------------------------------
! Local variables declaration
! ----------------------------------------------------------------------
      REAL (KIND = prec_d) :: ERP_igu_data(2,EOP_MAX_ARRAY), EOP_data(EOP_MAX_ARRAY), ERP_int(EOP_MAX_ARRAY)
      LOGICAL :: igu_flag
      INTEGER (KIND = prec_int8) :: mjd_UTC_day
      REAL (KIND = prec_d) :: mjd_ar(2), Xpole_ar(2), Ypole_ar(2), UT1UTC_ar(2), LOD_ar(2)
      REAL (KIND = prec_d) :: Xerr_ar(2), Yerr_ar(2), UT1err_ar(2), LODerr_ar(2)
      REAL (KIND = prec_d) :: mjd_int, Xpole_int, Ypole_int, UT1UTC_int, LOD_int
      REAL (KIND = prec_d) :: Xerr_int, Yerr_int, UT1err_int, LODerr_int
      REAL (KIND = prec_d) :: dX_eop, dY_eop
      INTEGER (KIND = prec_int2) :: i, sz1_EOP, sz2_EOP
! ----------------------------------------------------------------------



! ----------------------------------------------------------------------
! ERP data reading 
      CALL erp_igu (ERP_fname, mjd, ERP_igu_data, igu_flag)
      !if (igu_flag == .FALSE.) then
      if (igu_flag .EQV. .FALSE.) then
         !PRINT *,"--------------------------------------------------------"
         !PRINT *, "Warning error: Subroutine erp_igu.f90"
         !PRINT *, "Input epoch is out of the range covered by the IGS ultra-rapid ERP file" 
         !PRINT *, "Check the input iguwwwwd_hh.erp file"
         !PRINT *,"--------------------------------------------------------"
         !!STOP  ! END PROGRAM
      end if		 
! ----------------------------------------------------------------------

 
! ----------------------------------------------------------------------
! ERP interpolation
      mjd_int = mjd
      mjd_ar    = ERP_igu_data(1:2,EOP_MJD)
      Xpole_ar  = ERP_igu_data(1:2,EOP_X)
      Ypole_ar  = ERP_igu_data(1:2,EOP_Y)
      UT1UTC_ar = ERP_igu_data(1:2,EOP_UT1)
      LOD_ar    = ERP_igu_data(1:2,EOP_LOD)
      Xerr_ar = ERP_igu_data(1:2,EOP_X_ERR)
      Yerr_ar = ERP_igu_data(1:2,EOP_Y_ERR)
      UT1err_ar = ERP_igu_data(1:2,EOP_UT1_ERR)
      LODerr_ar = ERP_igu_data(1:2,EOP_LOD_ERR)
      CALL interp_lin (mjd_ar, Xpole_ar , mjd_int, Xpole_int)
      CALL interp_lin (mjd_ar, Ypole_ar , mjd_int, Ypole_int)
      CALL interp_lin (mjd_ar, UT1UTC_ar, mjd_int, UT1UTC_int)
      CALL interp_lin (mjd_ar, LOD_ar   , mjd_int, LOD_int)
      CALL interp_lin (mjd_ar, Xerr_ar   , mjd_int, Xerr_int)
      CALL interp_lin (mjd_ar, Yerr_ar   , mjd_int, Yerr_int)
      CALL interp_lin (mjd_ar, UT1err_ar   , mjd_int, UT1err_int)
      CALL interp_lin (mjd_ar, LODerr_ar   , mjd_int, LODerr_int)

      ERP_int (EOP_MJD) = mjd_int
      ERP_int (EOP_X) = Xpole_int
      ERP_int (EOP_Y) = Ypole_int
      ERP_int (EOP_UT1) = UT1UTC_int
      ERP_int (EOP_LOD) = LOD_int
      ERP_int (EOP_X_ERR) = Xerr_int
      ERP_int (EOP_Y_ERR) = Yerr_int
      ERP_int (EOP_UT1_ERR) = ut1err_int
      ERP_int (EOP_LOD_ERR) = LODerr_int
! ----------------------------------------------------------------------


! ----------------------------------------------------------------------
! dX,dY : Corrections w.r.t Precession-Nutation model
      !mjd_UTC_day = INT (mjd)
      !CALL eop_finals2000A (EOP_fname, mjd_UTC_day , EOP_data)
      !dX = EOP_data(6) 
      !dY = EOP_data(7) 
      !----------------------------------------------------------
      ! init next two var to something sensible
dX_eop = 0.d0
dY_eop = 0.d0
sz1_EOP = SIZE (EOP_days,DIM=1)
sz2_EOP = SIZE (EOP_days,DIM=2)
DO i = 1 , sz1_EOP  
If (mjd_int == EOP_days(i,EOP_MJD) ) then
! dX,dY (arcsec)													
      dX_eop = EOP_days(i,EOP_DX)
      dY_eop = EOP_days(i,EOP_DY)
End If
END DO
! ----------------------------------------------------------------------


! ----------------------------------------------------------------------
      EOP_int (EOP_MJD) = mjd_int
      EOP_int (EOP_X) = Xpole_int
      EOP_int (EOP_Y) = Ypole_int
      EOP_int (EOP_UT1) = UT1UTC_int
      EOP_int (EOP_LOD) = LOD_int
	  ! dX,dY : Precession-Nutation model corrections
      EOP_int (EOP_DX) = dX_eop !EOP_data (6) 
      EOP_int (EOP_DY) = dY_eop !EOP_data (7) 
! ----------------------------------------------------------------------
      EOP_int (EOP_X_ERR) = Xerr_int
      EOP_int (EOP_Y_ERR) = Yerr_int
      EOP_int (EOP_UT1_ERR) = ut1err_int
      EOP_int (EOP_LOD_ERR) = LODerr_int


!      PRINT *,"--------------------------------------------------------"
!      PRINT *, "ERP_igu_data"
!      PRINT *, ERP_igu_data
!      PRINT *, "ERP_int"
!      PRINT *, ERP_int
!      PRINT *,"--------------------------------------------------------"


	  
END SUBROUTINE


END
