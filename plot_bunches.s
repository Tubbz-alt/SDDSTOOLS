sddsprocess $1.out $1.tmp -noWarnings \
 "-define=column,dp/p,p pCentral - pCentral / 100 *,units=%" \
 "-process=t,average,tbar" \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-3 *,units=MeV" \
 "-process=E,average,Ebar" \
 "-define=column,z,t tbar - 2.99792458E11 *,units=mm" \
 "-filter=column,z,-2,2"

sddsprocess $1.tmp -noWarnings \
 "-process=z,standardDeviation,stdz" \
 "-print=param,zLabel,rms=%.3g %s,stdz,stdz.units" \
 "-process=dp/p,standardDeviation,stdp" \
 "-print=param,pLabel,rms=%.3g %s,stdp,stdp.units" \
 "-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units"

sddshist $1.tmp $1.zhis -data=z -sizeOfBins=0.005
sddshist $1.tmp $1.dhis -data=dp/p -bins=500
sddshist2d $1.tmp $1.zdhis -col=z,dp/p -xparam=200 -yparam=200 -smooth=4

sddsplot $2 $3 $4 $5 $6 $7 $8 $9 \
  -groupby=fileindex \
  -split=page -sep=tag \
  -layout=2,2,limit=3 \
  -column=z,dp/p $1.tmp -graph=dot -sparse=10 -tag=1 -topline=@ELabel -scale=0,0,0,0 \
  -column=frequency,dp/p $1.dhis -graph=yimpulse,type=1 -unsup=x \
  -xlabel=N -tag=2 -topline="E-Spectrum" \
  -column=z,frequency $1.zhis -graph=impulse,type=2 -unsup=y \
  -ylabel=N -tag=3 -topline="Microbunches" \
  "-title= Masked Beam @ $1" \
  -dateStamp
  
# sddscontour $1.zdhis -shade $2 $3 $4 $5 $6 $7 $8 $9


# rm tmp*.*
rm $1.dhis*
# rm $1.zhis*
rm $1.tmp*
rm $1.zdhis




