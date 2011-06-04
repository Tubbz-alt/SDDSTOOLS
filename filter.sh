#!/bin/sh

##################################################
#
# filter.sh
# =======
#
# Applies longitudinal (time and momentum)
# filter to an sdds beam file.
#
# ------------------------------------------------
#
# Usage
# =====
#
# filter.sh input_file [output_file]
#
# ------------------------------------------------
#
# Arguments
# =========
#
# input_file : Elegant formatted sdds file to
#              which the filter will be applied.
#
# output_file: Elegant formatted sdds file that
#              is the result of the filter.
#
##################################################

# usage
if ! ( [ $1 ] ); then
    echo "usage:"
    echo "addt.sh input_file [output_file]"
    exit 1
fi

input=$1
# if output file is not specified,
# set equal to input file
if ! ( [ $2 ] ); then
    output=$1
else
    output=$2
fi

# filter by time and momentum->
# remove particles outside of 10 std. dev.
sddsoutlier $input $output -noWarnings \
    -columns=t,p -stDevLimit=10.0

# clean up
if [ -e $input~ ]; then
    rm $input~
fi
