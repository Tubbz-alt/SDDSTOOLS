#!/bin/sh

##################################################
#
# metasim.sh
# =============
#
# Runs an Elegant simulation which contains only
# a single SCRIPT type element of zero length
# that calls the script "sim_shower.sh" to run
# a shower simulation. This script is intended for
# demonstrative purposes only.
#
# ------------------------------------------------
#
# Usage
# =====
#
# metasim.sh script.sh input_file output_file \
#   geometry_file [delta_limit]
#
# ------------------------------------------------
#
# Arguments
# =========
#
# script.sh    : The script that will be used to
#                run the Shower simulation.
#                NOTE: This argument must include
#                the full path for the script.
#                e.g. './sim_shower.sh'.
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
if ! ( [ $1 ] && [ $2 ] && [ $3 ] && [ $4 ] ); then
    echo "usage:"
    echo "metasim.sh script.sh input_file output_file"\
         "geometry_file [delta_limit]"
    exit 1
fi

# define variables from arguments
script=$1
input=$2
output=$3
geom=$4
geom_base=${geom%.*}
limit=$5

# set environment variables
export SHOWSCRIPT=$script
export SHOWIN=$input
export SHOWOUT=$output
export SHOWROOT=$geom_base
export SHOWGEOM=$geom
export SHOWFILT=$limit
elegant ./shower.ele
