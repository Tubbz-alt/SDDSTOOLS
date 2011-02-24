#!/bin/sh

###########################################
#
# plot_scat.sh
#
# Generates a scatter plot and projection
# plots along the two axes. No fits are
# peformed.
#
# NOTE: Can be used with 'plot_core.sh'.
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_scat.sh data.sdds xvar yvar \
#   [xlow] [xhigh] [ylow] [yhigh]
#
# -----------------------------------------
#
# Arguments
# =========
#
# data.sdds : SDDS file from which the data
#             is to be extracted. Expected
#             to be output from Elegant.
#             If the file's extension is
#             either '.sdds', or '.out',
#             it may be omitted.
#
# xvar      : Variable to be plotted along
#             the x-axis.
#
# yvar      : Variable to be plotted along
#             the y-axis.
#
# Possible values for 'xvar' and 'yvar':
#   x, xp, y, yp, z, d
#   where xp = x', yp = y', and d = dp/p
#
# xlow      : Lower bound on x-axis.
#
# xhigh     : Upper bound on x-axis.
#
# ylow      : Lower bound on y-axis.
#
# yhigh     : Upper bound on y-axis.
#
# Units for lower/upper bounds:
#
#   x,y,z: mm
#   xp,yp: mrad
#   d    : %
#
###########################################

# define variables from arguments
data_base=${1%.*}
xvar=$2
yvar=$3
xlow=$4
xhigh=$5
ylow=$6
yhigh=$7

# get full data file name
if [ "$1" == "$data_base" ];then
    if [ -e $data_base.out ]; then
	data=$data_base.out
    fi
    if [ -e $data_base.sdds ]; then
	data=$data_base.sdds
    fi
else
    data=$1
fi

# unit conversion and definition of columns
sddsprocess $data $data_base.tmp -noWarnings \
 "-convertUnits=column,x,mm,m,1.e3" \
 "-convertUnits=column,xp,mrad,,1.e3" \
 "-convertUnits=column,y,mm,m,1.e3" \
 "-convertUnits=column,yp,mrad,,1.e3" \
 "-process=t,average,tbar" \
 "-define=column,z,t tbar - 2.99792458E11 *,units=mm" \
 "-define=column,d,p pCentral - pCentral / 100 *,units=%"

if [ $xlow ] && [ $xhigh ]; then
    sddsprocess $data_base.tmp -noWarnings \
	"-filter=column,$xvar,$xlow,$xhigh"
fi

if [ $ylow ] && [ $yhigh ]; then
    sddsprocess $data_base.tmp -noWarnings \
	"-filter=column,$yvar,$ylow,$yhigh"
fi

# calculate rms values
sddsprocess $data_base.tmp -noWarnings \
 "-process=x,standardDeviation,xrms" \
 "-process=xp,standardDeviation,xprms" \
 "-process=y,standardDeviation,yrms" \
 "-process=yp,standardDeviation,yprms" \
 "-process=z,standardDeviation,zrms" \
 "-process=d,standardDeviation,drms"

# create labels
sddsprocess $data_base.tmp -noWarnings \
 "-define=column,E,p sqr 1 - sqrt 510.99906e-6 *,units=GeV" \
 "-process=E,average,Ebar" \
 "-print=param,ELabel,E\$b0\$n=%.3g %s,Ebar,Ebar.units" \
 "-print=param,xrmsLabel,\$gs\$r\$bx\$n=%.3g %s,xrms,xrms.units" \
 "-print=param,xprmsLabel,\$gs\$r\$bxp\$n=%.3g %s,xprms,yprms.units" \
 "-print=param,yrmsLabel,\$gs\$r\$by\$n=%.3g %s,yrms,yrms.units" \
 "-print=param,yprmsLabel,\$gs\$r\$byp\$n=%.3g %s,yprms,yprms.units" \
 "-print=param,zrmsLabel,\$gs\$r\$bz\$n=%.3g %s,zrms,zrms.units" \
 "-print=param,drmsLabel,\$gs\$r\$b\$gd\$r\$n=%.3g %s,drms,drms.units"

# create histograms
sddshist $data_base.tmp $data_base.xhis  -data=x  -bin=100
sddshist $data_base.tmp $data_base.xphis -data=xp -bin=100
sddshist $data_base.tmp $data_base.yhis  -data=y  -bin=100
sddshist $data_base.tmp $data_base.yphis -data=yp -bin=100
sddshist $data_base.tmp $data_base.zhis  -data=z  -bin=100
sddshist $data_base.tmp $data_base.dhis  -data=d  -bin=100

# generate the plots
sddsplot -groupby=fileindex \
  -split=page -sep=tag \
  -layout=2,2,limit=3 \
  -column=${xvar},${yvar} $data_base.tmp -graph=dot,type=3 \
      -tag=1 -sparse=1 -topline=@ELabel \
  -column=frequency,${yvar} $data_base.${yvar}his \
      -graph=yimpulse,type=2 -unsup=x -xlabel=N \
      -tag=2 \
  -column=${xvar},frequency $data_base.${xvar}his \
      -graph=impulse,type=1 -unsup=y -ylabel=N \
      -tag=3 \

# clean up
rm $data_base.tmp*
rm $data_base.*his*
