#!/bin/csh -f

sddshist $1 $1.hx -data=x -bins=200 
sddshist $1 $1.hyp -data=yp -bins=200

set ypMin = `sddsprocess $1 -pipe=out -process=yp,min,ypMin | sdds2stream -pipe -parameter=ypMin`
set ypMax = `sddsprocess $1 -pipe=out -process=yp,max,ypMax | sdds2stream -pipe -parameter=ypMax`

set dx = `sddsprocess $1 -pipe=out -process=x,spread,xSpread "-define=parameter,dx,xSpread 199 /" | sdds2stream -pipe -parameter=dx`

sddssort $1 -pipe=out -column=x,incr \
 | sddsbreak -pipe -change=x,amount=$dx \
 | sddsprocess -pipe -process=x,ave,xAve \
 | sddshist -pipe -data=yp -bins=200 -lower=$ypMin -upper=$ypMax \
 | sddsprocess -pipe -define=column,x,xAve,units=m \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-x-yp -column=frequency,decr

sddsplot -layout=2,2 \
         -column=x,yp $1.h-x-yp -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,yp $1.hyp \
         -end \
         -column=x,frequency $1.hx

