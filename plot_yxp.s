#!/bin/csh -f

sddshist $1 $1.hy -data=y -bins=200 
sddshist $1 $1.hxp -data=xp -bins=200

set xpMin = `sddsprocess $1 -pipe=out -process=xp,min,xpMin | sdds2stream -pipe -parameter=xpMin`
set xpMax = `sddsprocess $1 -pipe=out -process=xp,max,xpMax | sdds2stream -pipe -parameter=xpMax`

set dy = `sddsprocess $1 -pipe=out -process=y,spread,ySpread "-define=parameter,dy,ySpread 199 /" | sdds2stream -pipe -parameter=dy`

sddssort $1 -pipe=out -column=y,incr \
 | sddsbreak -pipe -change=y,amount=$dy \
 | sddsprocess -pipe -process=y,ave,yAve \
 | sddshist -pipe -data=xp -bins=200 -lower=$xpMin -upper=$xpMax \
 | sddsprocess -pipe -define=column,y,yAve,units=m \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-y-xp -column=frequency,decr

sddsplot -layout=2,2 \
         -column=y,xp $1.h-y-xp -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,xp $1.hxp \
         -end \
         -column=y,frequency $1.hy

