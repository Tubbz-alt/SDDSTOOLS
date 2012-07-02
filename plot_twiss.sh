#!/bin/sh

###########################################
#
# plot_twiss.sh
#
# Plots the beta and eta functions in x
# and y along the beamline. Overlays the
# floormap of the beamline for reference.
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_twiss.sh data.twi [data.mag]
#
# -----------------------------------------
#
# Arguments
# =========
#
# data.twi : Twiss output file produced by
#            an Elegant simulation. The
#            file extension '.twi' may be
#            omitted.
#
# data.mag : Magnet output file produced by
#            an Elegant simulation. If the
#            base name of this file is the
#            same as that of 'data.twi',
#            then this argument does not
#            need to be provided.
#
###########################################

# usage
if ! [ $1 ]; then
    echo "usage:"
    echo "plot_twiss.sh data.twi [data.mag]"
    exit 1
fi

# define variables from arguments
twiss_base=${1%.*}
twiss=$twiss_base.twi
if [ $2 ]; then
    mag=$2
else
    mag=$twiss_base.mag
fi

# generate the plot
sddsplot \
    -column=s,beta? -legend=ysymbol -dateStamp -unsup=y \
    -zoom=yfac=0.87,qcent=0.53 $twiss -graphics=line,vary -yscale=id=1 \
    -title="Twiss parameters for $twiss" \
    -column=s,eta? -legend=ysymbol -unsup=y \
    -zoom=yfac=0.87,qcent=0.53 $twiss -graphic=line,vary -yscale=id=2 \
    -column=s,Profile $mag \
    -overlay=xmode=normal,yfactor=0.05,qoffset=0.43,ycenter,ymode=unit \
