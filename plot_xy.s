sddsprocess $1 $1.tmp \
 "-convertUnits=column,x,mm,m,1.e3" \
 "-convertUnits=column,y,mm,m,1.e3"

sddsprocess $1.tmp -noWarnings \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-6 *,units=GeV" \
 "-process=E,average,Ebar" \
 "-process=x,standardDeviation,xrms" \
 "-process=y,standardDeviation,yrms" \
 "-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units" \
 "-print=param,xrmsLabel,\$gs\$r\$bx\$n=%.3g %s,xrms,xrms.units" \
 "-print=param,yrmsLabel,\$gs\$r\$by\$n=%.3g %s,yrms,yrms.units"

sddshist $1.tmp $1.zhis -data=x -bin=100
sddshist $1.tmp $1.dhis -data=y -bin=100

sddsplot $2 $3 $4 $5 $6 -groupby=fileindex \
  -split=page -sep=tag \
  -layout=2,2,limit=3 \
  -column=x,y $1.tmp -graph=dot,type=3 -tag=1 -sparse=1 -topline=@ELabel -scale=0,0,0,0 \
  -column=frequency,y $1.dhis -graph=yimpulse,type=1 -unsup=x -xlabel=N -tag=2 -topline=@yrmsLabel -scale=0,0,0,0 \
  -column=x,frequency $1.zhis -graph=impulse,type=2 -unsup=y -ylabel=N -tag=3 -topline=@xrmsLabel -scale=0,0,0,0 \
  -dateStamp

rm *.tmp*
rm *.dhis
rm *.zhis
