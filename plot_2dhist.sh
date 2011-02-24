#!/bin/sh

###########################################
#
# plot_2dhist.sh
#
# Generates a 2-D histogram.
#
# NOTE: Can be used with 'plot_core.sh'.
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_2dhist.sh data.sdds xvar yvar \
#   [conts] [xbins] [ybins] \
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
# conts     : Number of contour colors to
#             be used. Default = 50.
#
# xbins     : Number of bins to use along
#             the x-axis. Default = 100.
#
# ybins     : Number of bins to use along
#             the y-axis. Default = 100.
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
if [ $4 ]; then
    conts=$4
else
    conts=50
fi
if [ $5 ]; then
    xbins=$5
else
    xbins=100
fi
if [ $6 ]; then
    ybins=$6
else
    ybins=100
fi
xlow=$7
xhigh=$8
ylow=$9
yhigh=${10}

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

# clean up
if [ -e $data_base.tmp ]; then
    rm $data_base.tmp
fi
if [ -e $data_base.2dhis ]; then
    rm $data_base.2dhis
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

# create 2-D histogram
sddshist2d $data_base.tmp $data_base.2dhis \
    -col=$xvar,$yvar -xpar=$xbins -ypar=$ybins

# draw color plot of 2-D histogram
sddscontour $data_base.2dhis -quantity=frequency \
    -shade=32 -contours=$conts -topline=""

# clean up
if [ -e $data_base.tmp ]; then
    rm $data_base.tmp
fi
if [ -e $data_base.2dhis ]; then
    rm $data_base.2dhis
fi
