sddsprocess $1.sig $1.tmp -noWarnings \
 "-redefine=column,Sx,Sx 1E3 *,units=mm" \
 "-redefine=column,Sy,Sy 1E3 *,units=mm" \
 "-redefine=column,Ss,Ss 1E3 *,units=mm" \

sddsplot \
		 $2 $3 $4 $5 $6 -column=s,"(Sx,Sy)" -legend=ysymbol -dateStamp -unsup=y \
             -zoom=yfac=0.87,qcent=0.53 $1.tmp -graphics=line,vary -yscale=id=1 \
             "-title= Beam Sizes for $1" \
             -column=s,Profile $1.mag \
             -overlay=xmode=normal,yfactor=0.05,qoffset=0.43,ycenter,ymode=unit
             
# rm $1.tmp*

#             -column=s,Ss -legend=ysymbol -unsup=y \
#             -zoom=yfac=0.87,qcent=0.53 $1.tmp -graphic=line,vary -yscale=id=2 \
