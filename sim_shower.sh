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
if [ -e $input_base.show ]; then
    rm $input_base.show
fi
./ele2show.sh $input $input_base.show

# run shower
shower $input_base.show -geometry=$geom -samples=1 -keep=electrons -root=$geom_base -summary >& $geom_base.log

# convert output shower file to elegant file
if [ -e $geom_base.tmp ]; then
    rm $geom_base.tmp
fi
./show2ele.sh $geom_base.show $geom_base.tmp

# add temporal profile back into the output file
./addt.sh $geom_base.tmp $input

# filter stray particles
if [ -e $output ]; then
    rm $output
fi
export FILTREF=$input
export FILTARG=$filt_arg
export FILTIN=$geom_base.tmp
export FILTOUT=$output
elegant ./filter.ele

# clean up
if [ -e $geom_base.tmp ]; then
    rm $geom_base.tmp
fi
