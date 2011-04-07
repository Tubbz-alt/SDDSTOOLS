#!/bin/sh

###########################################
#
# plot_cent.sh
#
# Plots the centroids of the beam along
# the beamline. Overlays the floormap of
# the beamline for reference.
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_cent.sh data.cen [data.mag]
#
# -----------------------------------------
#
# Arguments
# =========
#
# data.cen : Centroid output file produced by
#            an Elegant simulation. The
#            file extension '.cen' may be
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
    echo "plot_cen.sh data.cen [data.mag]"
    exit 1
fi

# define variables from arguments
cent_base=${1%.*}
cent=$cent_base.cen
if [ $2 ]; then
    mag=$2
else
    mag=$cent_base.mag
fi

# unit conversion
sddsprocess $cent $cent_base.tmp -noWarnings \
 "-convertUnits=column,Cx,mm,m,1.e3" \
 "-convertUnits=column,Cy,mm,m,1.e3"

# generate the plot
sddsplot \
    -column=s,Cx -legend=ysymbol -dateStamp -unsup=y \
    -zoom=yfac=0.87,qcent=0.53 $cent_base.tmp -graphics=line,vary -yscale=id=1 \
    -title="Cent parameters for $cent" \
    -column=s,Cy -legend=ysymbol -unsup=y \
    -zoom=yfac=0.87,qcent=0.53 $cent_base.tmp -graphic=line,vary -yscale=id=2 \
    -column=s,Profile $mag \
    -overlay=xmode=normal,yfactor=0.05,qoffset=0.43,ycenter,ymode=unit \
