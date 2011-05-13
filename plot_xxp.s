#!/bin/csh -f

sddshist $1 $1.hx -data=x -bins=200 
sddshist $1 $1.hxp -data=xp -bins=200

set xpMin = `sddsprocess $1 -pipe=out -process=xp,min,xpMin | sdds2stream -pipe -parameter=xpMin`
set xpMax = `sddsprocess $1 -pipe=out -process=xp,max,xpMax | sdds2stream -pipe -parameter=xpMax`

set dx = `sddsprocess $1 -pipe=out -process=x,spread,xSpread "-define=parameter,dx,xSpread 199 /" | sdds2stream -pipe -parameter=dx`

sddssort $1 -pipe=out -column=x,incr \
 | sddsbreak -pipe -change=x,amount=$dx \
 | sddsprocess -pipe -process=x,ave,xAve \
 | sddshist -pipe -data=xp -bins=200 -lower=$xpMin -upper=$xpMax \
 | sddsprocess -pipe -define=column,x,xAve,units=m \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-x-xp -column=frequency,decr

sddsplot -layout=2,2 \
         -column=x,xp $1.h-x-xp -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,xp $1.hxp \
         -end \
         -column=x,frequency $1.hx
