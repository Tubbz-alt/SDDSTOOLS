#!/bin/sh  

##################################################
#
# ele2show.sh
# ===========
#
# Converts Elegant formatted sdds file into
# Shower formatted sdds file.
#
# ------------------------------------------------
#
# Usage
# =====
#
# ele2show.sh elegant_file [shower_file] [part_type]
#
# ------------------------------------------------
#
# Arguments
# =========
#
# elegant_file : Elegant formatted sdds file to be
#                converted to Shower format.
#
# shower_file  : Name of new Shower formatted sdds
#                file.
#
# part_type    : Type of particle to keep. Possible
#                values: 'electrons' or 'positrons'.
#                Default is 'electrons'.
#
##################################################

# usage
if ! ( [ $1 ] ); then
    echo "usage:"
    echo "ele2show.sh elegant_file [shower_file] [part_type]"
    exit 1
fi

input=$1
if ( [ $2 ] ); then
    output=$2
else
    output=$input
fi
if ( [ $3 ] ); then
    type=$3
else
    type='electrons'
fi

# NOTE: Sets 'z' equal to '0' for all particles.
#       Columns 'u' and 'v' are normalized angles.
sddsprocess $input -pipe=out \
    "-define=column,w,xp sqr yp sqr + 1 + sqrt rec" \
    "-define=column,u,xp w *" \
    "-define=column,v,yp w *" \
    "-define=column,Energy,p sqr 1 + sqrt mev *,units=MeV" \
    "-define=column,z,0,units=m" \
    "-reprint=parameter,Type,electrons" \
    | sddsconvert -pipe=in $output \
    -retain=column,u,v,w,x,y,z,Energy,t

# clean up
if [ -e $input~ ]; then
    rm $intput~
fi
