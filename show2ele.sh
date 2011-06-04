#!/bin/sh  

##################################################
#
# ele2show.sh
# ===========
#
# Converts Shower formatted sdds file into
# Elegant formatted sdds file.
#
# ------------------------------------------------
#
# Usage
# =====
#
# show2ele.sh shower_file [elegant_file] [part_type]
#
# ------------------------------------------------
#
# Arguments
# =========
#
# shower_file  : Shower formatted sdds file to be
#                converted to Elegant format.
#
# elegant_file : Name of new Elegant formatted sdds
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
    echo "show2ele.sh shower_file [elegant_file] [part_type]"
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

# NOTE: Adds new column 'deltat', which represents the
#       time of traversal across the geometry used in
#       the shower simulation.
sddsprocess $input -pipe=out -noWarning \
    -match=parameter,Type=$type \
    -filter=column,w,0.01,1.01 \
    "-define=column,xp,u w /" \
    "-define=column,yp,v w /" \
    "-define=column,p,Energy mev / sqr 1 - sqrt,units=m\$be\$nc" \
    "-define=column,vz,w c_mks *,units=m/s" \
    "-process=z,average,deltaz" \
    "-define=column,deltat,deltaz vz /,units=s" \
    | sddsconvert -pipe -retain=column,x,y,xp,yp,p,deltat,Particle \
    -retain=parameter,deltaz,Particles \
    | sddscombine -pipe=in $output -merge

# clean up
if [ -e $input~ ]; then
    rm $input~
fi
