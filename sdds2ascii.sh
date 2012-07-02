#!/bin/sh

###########################################
#
# sdds2ascii.sh
#
# Generates an ascii file from an sdds file.
#
# -----------------------------------------
#
# Usage
# =====
#
# sdds2ascii.sh input.sdds [output.ascii]
#
# -----------------------------------------
#
# Arguments
# =========
#
# input.sdds     : SDDS file to be converted to
#                  ascii format.
#
# [output.ascii] : Name of output ascii file.
#                  Automatically derived from
#                  input SDDS file name if not
#                  specified.
#
# Output Parameters in the order they appear:
#
#  pCentral [=gamma, no units]
#  Charge [C]
#  Particles [no units]
#
# Output Columns in the order they appear:
#
#  x    [m]
#  y    [m]
#  x'   [r]
#  y'   [r]
#  z    [m]
#  dp/p [no units]
#  t    [s]
#  p    [=gamma, no units]
#
###########################################

#usage
if ! ( [ $1 ] ); then
    echo "usage:"
    echo "sdds2ascii.sh input.sdds [output.ascii]"
    exit 1
fi

# define variables from arguments
input=$1
if ! [ $2 ];then
    output=${input%.*}
    output=$output.ascii
else
    output=$2
fi

# create the ascii file from the sdds file
sddsprocess $input -pipe=out \
    "-process=t,average,tbar" \
    "-define=column,z,t tbar - 2.99792458E8 *,units=m" \
    "-define=column,d,p pCentral - pCentral /" \
    | sdds2plaindata -pipe=in $output \
    -outputMode=ascii "-separator= "\
    -parameter=pCentral -parameter=Charge -parameter=Particles \
    -column=particleID \
    -column=x -column=y -column=xp -column=yp \
    -column=z -column=d -column=t -column=p
