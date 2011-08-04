#!/bin/csh -f

sddshist $1 $1.hy -data=y -bins=200 
sddshist $1 $1.hyp -data=yp -bins=200

set ypMin = `sddsprocess $1 -pipe=out -process=yp,min,ypMin | sdds2stream -pipe -parameter=ypMin`
set ypMax = `sddsprocess $1 -pipe=out -process=yp,max,ypMax | sdds2stream -pipe -parameter=ypMax`

set dy = `sddsprocess $1 -pipe=out -process=y,spread,ySpread "-define=parameter,dy,ySpread 199 /" | sdds2stream -pipe -parameter=dy`

sddssort $1 -pipe=out -column=y,incr \
 | sddsbreak -pipe -change=y,amount=$dy \
 | sddsprocess -pipe -process=y,ave,yAve \
 | sddshist -pipe -data=yp -bins=200 -lower=$ypMin -upper=$ypMax \
 | sddsprocess -pipe -define=column,y,yAve,units=m \
 | sddscombine -pipe -merge \
 | sddsnormalize -pipe -column=frequency \
 | sddssort -pipe=in $1.h-y-yp -column=frequency,decr

sddsplot -layout=2,2 \
         -column=y,yp $1.h-y-yp -split=column=frequency,width=0.01 -graph=sym,type=2,vary=subtype,fill -order=spectral \
         -end \
         -column=frequency,yp $1.hyp \
         -end \
         -column=y,frequency $1.hy
