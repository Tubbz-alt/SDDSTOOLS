&initial_coordinates &end

!--------------------------------------
! Notch Collimator Geometry
!
! R56 = 10mm configuration
!--------------------------------------

! - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
! Empty volume upstream of collimator (do not remove).
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
&block label="Vacuum upstream of collimator"  material="Vacuum"
   z_lower_cm=    -1 z_upper_cm=   0.0
   x_lower_cm=   -10 x_upper_cm= -0.05 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

! - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
! Notch Collimator (begins at z=0)
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
&block label="Left Tantalum collimator"       material="Ta"
   z_lower_cm=   0.0 z_upper_cm=     1 z_slices= 1
   x_lower_cm=   -10 x_upper_cm= -0.05 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

&block label="Vacuum left of tantalum blade"  material="Vacuum" 
   z_lower_cm=   0.0 z_upper_cm=     1
   x_lower_cm= -0.05 x_upper_cm= 0.055 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

&block label="Tantalum blade"                 material="Ta"
   z_lower_cm=   0.0 z_upper_cm=     1 z_slices= 1
   x_lower_cm= 0.055 x_upper_cm= 0.105 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

&block label="Vacuum right of tantalum blade" material="Vacuum" 
   z_lower_cm=   0.0 z_upper_cm=     1
   x_lower_cm= 0.105 x_upper_cm=   0.5 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

&block label="Right Tantalum collimator"      material="Ta"
   z_lower_cm=   0.0 z_upper_cm=     1 z_slices= 1
   x_lower_cm=   0.5 x_upper_cm=    10 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

&block label="Drift space"                    material="Vacuum"
   z_lower_cm=     1 z_upper_cm=    10 
   x_lower_cm=   -10 x_upper_cm=    10 
   y_lower_cm=   -10 y_upper_cm=    10 
&end

! - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
! Volume for gathering particle coordinates of forward beam.
! - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
&block label="Output volume" material="Vacuum"  
   outputfile="%s.show"
   z_lower_cm=    10 z_upper_cm=   100 
   x_lower_cm=   -10 x_upper_cm=    10 
   y_lower_cm=   -10 y_upper_cm=    10 
&end
