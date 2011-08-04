#!/bin/csh -f

sddsprocess $1 $1.tmp -noWarnings \
 "-define=column,dp/p,p pCentral - pCentral / 100 *,units=%" \
 "-process=t,average,tbar" \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-3 *,units=MeV" \
 "-process=E,average,Ebar" \
 "-redefine=column,x,x 1E3 *,units=mm" \
 "-filter=column,dp/p,-4,4"

sddsprocess $1.tmp -noWarnings \
 "-process=x,standardDeviation,stdx" \
 "-process=dp/p,standardDeviation,stdp" \

sddshist $1.tmp $1.hx -data=x -bins=200 
sddshist $1.tmp $1.hdpp -data=dp/p -bins=200

set dppMin = `sddsprocess $1.tmp -pipe=out -process=dp/p,min,dppMin | sdds2stream -pipe -parameter=dppMin`
set dppMax = `sddsprocess $1.tmp -pipe=out -process=dp/p,max,dppMax | sdds2stream -pipe -parameter=dppMax`

set dx = `sddsprocess $1.tmp -pipe=out -process=x,spread,xSpread "-define=parameter,dx,xSpread 199 /" | sdds2stream -pipe -parameter=dx`

sddssort $1.tmp -pipe=out -column=x,incr \
 | sddsbreak -pipe -change=x,amount=$dx \
 | sddsprocess -pipe -process=x,ave,xAve \
 | sddshist -pipe -data=dp/p -bins=200 -lower=$dppMin -upper=$dppMax \
 | sddsprocess -pipe -define=column,x,xAve,units=mm \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-x-dp -column=frequency,decr

sddsplot -layout=2,2 \
         -column=x,dp/p $1.h-x-dp -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,dp/p $1.hdpp \
         -end \
         -column=x,frequency $1.hx
