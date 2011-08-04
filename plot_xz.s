sddsprocess $1.out $1.tmp \
 "-convertUnits=column,x,mm,m,1.e3" \
 "-process=t,average,tbar" \
 "-define=column,z,t tbar - 2.99792458E11 *,units=mm"
# "-filter=column,z,-2,3"

sddsprocess $1.tmp -noWarnings \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-6 *,units=GeV" \
 "-process=E,average,Ebar" \
 "-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units"

sddsplot $2 $3 $4 $5 $6 -groupby=fileindex \
  -split=page -sep=tag \
  -layout=2,2,limit=3 \
  -column=x,z $1.tmp -graph=sym,type=2,vary=subtype,fill -tag=1 -sparse=1 -topline=@ELabel \
  -dateStamp

rm tmp*.*
rm *.tmp*
rm *.xhis*
rm *.yhis*
rm *.gfit*
