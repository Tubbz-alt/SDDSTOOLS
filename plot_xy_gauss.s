sddsprocess $1 $1.tmp \
 "-convertUnits=column,x,mm,m,1.e3" \
 "-convertUnits=column,y,mm,m,1.e3"
# "-filter=column,x,-0.2,0.2" \
# "-filter=column,y,-0.2,0.2" 

sddsprocess $1.tmp -noWarnings \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-6 *,units=GeV" \
 "-process=E,average,Ebar" \
 "-process=x,standardDeviation,xrms" \
 "-process=y,standardDeviation,yrms" \
 "-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units" \
 "-print=param,xrmsLabel,\$gs\$r\$bx\$n=%.3g %s,xrms,xrms.units" \
 "-print=param,yrmsLabel,\$gs\$r\$by\$n=%.3g %s,yrms,yrms.units"

sddshist $1.tmp $1.xhis -data=x -bin=100
sddshist $1.tmp $1.yhis -data=y -bin=100

sddsgfit $1.xhis xhis.gfit -column=x,frequency
sddsgfit $1.yhis yhis.gfit -column=y,frequency

sddsprocess xhis.gfit -noWarnings \
 "-print=param,Sxg,\$gs\$r\$bx\$n=%.3g %s,gfitSigma,gfitSigma.units"

sddsprocess yhis.gfit -noWarnings \
 "-print=param,Syg,\$gs\$r\$by\$n=%.3g %s,gfitSigma,gfitSigma.units"

sddsxref $1.xhis xhis.gfit -transfer=parameter,Sxg,gfitSigma -noWarning
sddsxref $1.yhis yhis.gfit -transfer=parameter,Syg,gfitSigma -noWarning

sddsplot $2 $3 $4 $5 $6 -groupby=fileindex \
  -split=page -sep=tag \
  -layout=2,2,limit=3 \
  -column=x,y $1.tmp -graph=dot,type=3 -tag=1 -sparse=1 -topline=@ELabel \
  -column=frequency,y $1.yhis -graph=yimpulse,type=2 -unsup=x -xlabel=N -tag=2 -topline=@Syg \
  -column=frequencyFit,y yhis.gfit -graph=line,type=4 -unsup=x -tag=2 \
  -column=x,frequency $1.xhis -graph=impulse,type=1 -unsup=y -ylabel=N -tag=3 -topline=@Sxg \
  -column=x,frequencyFit xhis.gfit -graph=line,type=5 -unsup=y -tag=3 \
  -dateStamp

rm tmp*.*
rm *.tmp*
rm *.xhis*
rm *.yhis*
rm *.gfit*
