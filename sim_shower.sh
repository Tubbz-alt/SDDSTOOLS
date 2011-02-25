#!/bin/sh

##################################################
#
# sim_shower.sh
# =============
#
# Runs a Shower simulation taking an Elegant
# formatted sdds input file and generating
# an Elegant formatted sdds output file with
# the correct longitudinal profile. Also removes
# stray particles with a momentum filter.
#
# ------------------------------------------------
#
# Usage
# =====
#
# sim_shower.sh input_file output_file \
#   geometry_file [delta_limit]
#
# ------------------------------------------------
#
# Arguments
# =========
#
# input_file   : Elegant formatted sdds file used
#                for input to Shower simulation.
#
# output_file  : Elegant formatted sdds output file
#                from Shower simulation.
#
# geometry_file: File specifying the geometry to be
#                used in Shower simulation.
#
# delta_limit  : Argument for momentum filter.
#                Particles satisfying
#                |dp/p| > delta_limit
#                will be removed. Default value
#                is 100, approximating no filter.
#                NOTE: The limit is not given as
#                a percentage.
#
# ------------------------------------------------
#
# NOTE: You _MUST_ define the 'outputfile' variable
#       in your geometry file to be "%s.show".
#
#       i.e. The definition of your collection
#       volume should include the line:
#
#       outputfile="%s.show"
#
##################################################

# usage
if ! ( [ $1 ] && [ $2 ] && [ $3 ] ); then
    echo "usage:"
    echo "sim_shower.sh input_file output_file"\
         "geometry_file [delta_limit]"
    exit 1
fi

# set SHOWERSIM directory, if not set
if ! [ $SHOWERSIM ]; then
    export SHOWERSIM=$PWD
fi

# define variables from arguments
input=$1
output=$2
geom=$3

# set basenames for files
input_base=${input%.*}
output_base=${output%.*}
geom_base=${geom%.*}

# momentum filter argument;
# use default value if not given
if [ $4 ]; then
    filt_arg=$4
else
    filt_arg=100.0
fi

# convert input elegant file to shower file
if [ -e $input_base.show.tmp ]; then
    rm $input_base.show.tmp
fi
$SHOWERSIM/ele2show.sh $input $input_base.show.tmp

# run shower
shower $input_base.show.tmp -geometry=$geom -samples=1 -keep=electrons -root=$geom_base -summary >& $geom_base.log

# convert output shower file to elegant file
if [ -e $geom_base.out.tmp ]; then
    rm $geom_base.out.tmp
fi
$SHOWERSIM/show2ele.sh $geom_base.show $geom_base.out.tmp

# add temporal profile back into the output file
$SHOWERSIM/addt.sh $geom_base.out.tmp $input

# filter stray particles
if [ -e $output ]; then
    rm $output
fi
export FILTREF=$input
export FILTARG=$filt_arg
export FILTIN=$geom_base.out.tmp
export FILTOUT=$output
elegant $SHOWERSIM/filter.ele

# clean up
if [ -e $input_base.show.tmp ]; then
    rm $input_base.show.tmp
fi
if [ -e $geom_base.show ]; then
    rm $geom_base.show
fi
if [ -e $geom_base.show.tmp ]; then
    rm $geom_base.show.tmp
fi
if [ -e $geom_base.out.tmp ]; then
    rm $geom_base.out.tmp
fi
if [ -e $geom_base.out.tmp~ ]; then
    rm $geom_base.out.tmp~
fi
