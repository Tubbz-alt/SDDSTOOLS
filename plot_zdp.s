#!/bin/csh -f

sddsprocess $1 $1.tmp -noWarnings \
 "-define=column,dp/p,p pCentral - pCentral / 100 *,units=%" \
 "-process=t,average,tbar" \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-3 *,units=MeV" \
 "-process=E,average,Ebar" \
 "-define=column,z,t tbar - 2.99792458E11 *,units=mm" \
 "-filter=column,z,-2,3"


sddsprocess $1.tmp -noWarnings \
 "-process=z,standardDeviation,stdz" \
 "-print=param,zLabel,rms=%.3g %s,stdz,stdz.units" \
 "-process=dp/p,standardDeviation,stdp" \

sddshist $1.tmp $1.hz -data=z -bins=200 
sddshist $1.tmp $1.hdpp -data=dp/p -bins=200

set dppMin = `sddsprocess $1.tmp -pipe=out -process=dp/p,min,dppMin | sdds2stream -pipe -parameter=dppMin`
set dppMax = `sddsprocess $1.tmp -pipe=out -process=dp/p,max,dppMax | sdds2stream -pipe -parameter=dppMax`

set dz = `sddsprocess $1.tmp -pipe=out -process=z,spread,zSpread "-define=parameter,dz,zSpread 199 /" | sdds2stream -pipe -parameter=dz`

sddssort $1.tmp -pipe=out -column=z,incr \
 | sddsbreak -pipe -change=z,amount=$dz \
 | sddsprocess -pipe -process=z,ave,zAve \
 | sddshist -pipe -data=dp/p -bins=200 -lower=$dppMin -upper=$dppMax \
 | sddsprocess -pipe -define=column,z,zAve,units=mm \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-z-dp -column=frequency,decr

sddsplot -layout=2,2 \
         -column=z,dp/p $1.h-z-dp -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,dp/p $1.hdpp \
         -end \
         -column=z,frequency $1.hz
