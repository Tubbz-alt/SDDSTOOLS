#!/bin/csh -f

sddsprocess $1 $1.tmp -noWarnings \
 "-define=column,dp/p,p pCentral - pCentral / 100 *,units=%" \
 "-process=t,average,tbar" \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-3 *,units=MeV" \
 "-process=E,average,Ebar" \
 "-redefine=column,x,x 1E3 *,units=mm" \
 "-redefine=column,y,y 1E3 *,units=mm" \
 "-filter=column,dp/p,-4,4"

sddsprocess $1.tmp -noWarnings \
 "-process=x,standardDeviation,stdx" \
 "-process=y,standardDeviation,stdy" \

sddshist $1.tmp $1.hx -data=x -bins=200 
sddshist $1.tmp $1.hy -data=y -bins=200

set yMin = `sddsprocess $1.tmp -pipe=out -process=y,min,yMin | sdds2stream -pipe -parameter=yMin`
set yMax = `sddsprocess $1.tmp -pipe=out -process=y,max,yMax | sdds2stream -pipe -parameter=yMax`

set dx = `sddsprocess $1.tmp -pipe=out -process=x,spread,xSpread "-define=parameter,dx,xSpread 199 /" | sdds2stream -pipe -parameter=dx`

sddssort $1.tmp -pipe=out -column=x,incr \
 | sddsbreak -pipe -change=x,amount=$dx \
 | sddsprocess -pipe -process=x,ave,xAve \
 | sddshist -pipe -data=y -bins=200 -lower=$yMin -upper=$yMax \
 | sddsprocess -pipe -define=column,x,xAve,units=mm \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-x-y -column=frequency,decr

sddsplot -layout=2,2 \
         -column=x,y $1.h-x-y -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,y $1.hy \
         -end \
         -column=x,frequency $1.hx
