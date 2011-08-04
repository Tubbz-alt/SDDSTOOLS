sddsplot \
		 $2 $3 $4 $5 $6 -column=s,beta* -legend=ysymbol -dateStamp -unsup=y \
             -zoom=yfac=0.87,qcent=0.53 $1.twi -graphics=line,vary -yscale=id=1 \
             "-title=Twiss parameters for $1" \
             -column=s,eta? -legend=ysymbol -unsup=y \
             -zoom=yfac=0.87,qcent=0.53 $1.twi -graphic=line,vary -yscale=id=2 \
             -column=s,Profile $1.mag \
             -overlay=xmode=normal,yfactor=0.05,qoffset=0.43,ycenter,ymode=unit
