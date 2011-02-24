#!/bin/sh

###########################################
#
# plot_line.sh
#
# Plots a floormap of the beamline.
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_line.sh data.mag [zoom]
#
# -----------------------------------------
#
# Arguments
# =========
#
# data.twi : Magnet output file produced by
#            an Elegant simulation. The
#            file extension '.mag' may be
#            omitted.
#
# zoom     : The zoom factor. Units are 
#            given in half-plot-height.
#            e.g. If zoom=1.0, the quads
#            will be drawn to reach the
#            upper (or lower) edge of the
#            plot. The default zoom value
#            is 0.5.
#
###########################################

# define variables from arguments
data_base=${1%.*}
mag=$data_base.mag
if [ $2 ]; then
    zoom=$2
else
    zoom=0.5
fi

sddsplot -column=s,Profile $mag -zoom=yfac=$zoom
