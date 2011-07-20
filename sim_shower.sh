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
#   geometry_file
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
# ------------------------------------------------
#
# NOTE: Set the environment variable SHOWERSIM to this 
#	directory if you plan on calling sim_shower.sh 
#	from another directory. This can be done by    
#	sourcing the SOURCEME file while inside this   
#	directory.				       
#						       
#	e.g.:					       
#						       
#	. ./SOURCEME
#
##################################################

# usage
if ! ( [ $1 ] && [ $2 ] && [ $3 ] ); then
    echo "usage:"
    echo "sim_shower.sh input_file output_file"\
         "geometry_file"
    exit 1
fi

# define variables from arguments
input=$1
output=$2
geom=$3

# set directory locations

# SHOWERSIM directory
if ! [ $SHOWERSIM ]; then
    SHOWERSIM=$PWD
fi

# set basenames for files
input_base=${input%.*}
input_base=${input_base##*/}
output_base=${output%.*}
output_base=${output_base##*/}
geom_base=${geom%.*}
geom_base=${geom_base##*/}

# define working directory
workdir=${output%.*}
workdir=${workdir%/*}
if [ "$workdir" == "$output_base" ]; then
    workdir=$SHOWERSIM
fi

#==========================================

# convert input elegant file to shower file
if [ -e $workdir/$input_base.show.tmp ]; then
    rm $workdir/$input_base.show.tmp
fi
$SHOWERSIM/ele2show.sh $input $workdir/$input_base.show.tmp

# run shower
shower $workdir/$input_base.show.tmp -geometry=$geom -samples=1 -keep=electrons -root=$workdir/$output_base -summary >& $workdir/$output_base.log

# clean up
if [ -e $PWD/fort.8 ]; then
    rm $PWD/fort.8
fi
if [ -e $workdir/$input_base.show.tmp ]; then
    rm $workdir/$input_base.show.tmp
fi

# convert output shower file to elegant file
if [ -e $output ]; then
    rm $output
fi
$SHOWERSIM/show2ele.sh $workdir/$output_base.show $output.tmp

# clean up
if [ -e $workdir/$output_base.show ]; then
    rm $workdir/$output_base.show
fi

# add temporal profile back into the output file
$SHOWERSIM/addt.sh $output.tmp $input

# filter stray particles
$SHOWERSIM/filter.sh $output.tmp $output

# clean up
if [ -e $output.tmp ]; then
    rm $output.tmp
fi
