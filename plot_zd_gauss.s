sddsprocess $1 $1.tmp -noWarnings \
 "-define=column,dp/p,p pCentral - pCentral / 100 *,units=%" \
 "-process=t,average,tbar" \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-3 *,units=MeV" \
 "-process=E,average,Ebar" \
 "-convertUnits=param,Ebar,GeV,MeV,1e-3" \
 "-define=column,z,t tbar - 2.99792458E11 *,units=mm" \
 "-filter=column,dp/p,-3,3"

sddsprocess $1.tmp -noWarnings \
 "-process=z,standardDeviation,stdz" \
 "-print=param,zLabel,rms=%.3g %s,stdz,stdz.units" \
 "-process=dp/p,standardDeviation,stdp" \
 "-print=param,pLabel,rms=%.3g %s,stdp,stdp.units" \
 "-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units"

sddshist $1.tmp $1.zhis -data=z -bin=500
sddshist $1.tmp $1.dhis -data=dp/p -bin=500

sddsgfit $1.zhis zhis.gfit -column=z,frequency
sddsgfit $1.dhis dhis.gfit -column=dp/p,frequency

sddsprocess zhis.gfit -noWarnings \
 "-print=param,Szg,\$gs\$r\$bz\$n=%.3g %s,gfitSigma,gfitSigma.units"

sddsprocess dhis.gfit -noWarnings \
 "-print=param,Sdg,\$gs\$r\$b\$gd\$r\$n=%.3g %s,gfitSigma,gfitSigma.units"

sddsxref $1.zhis zhis.gfit -transfer=parameter,Szg,gfitSigma -noWarning
sddsxref $1.dhis dhis.gfit -transfer=parameter,Sdg,gfitSigma -noWarning

sddsplot $2 $3 $4 $5 $6 $7 $8 $9 \
  -groupby=fileindex \
  -split=page -sep=tag \
  -layout=2,2,limit=3 \
  -column=z,dp/p $1.tmp -graph=dot,vary -sparse=10 -tag=1 -topline=@ELabel -scale=0,0,0,0 \
  -column=frequency,dp/p $1.dhis -graph=yimpulse,vary -unsup=x \
  -xlabel=N -tag=2 -topline=@pLabel \
  -column=z,frequency $1.zhis -graph=impulse,vary -unsup=y \
  -ylabel=N -tag=3 -topline=@Szg \
  -column=z,frequencyFit $1.zhis -graph=line,type=1 -unsup=y -tag=3 \
  -dateStamp

rm tmp*.*
rm $1.dhis*
# rm $1.zhis*
rm $1.tmp*
rm *.gfit*
