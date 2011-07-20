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
# filter.sh input_file output_file
#
# ------------------------------------------------
#
# Arguments
# =========
#
# input_file    : Elegant formatted sdds file to
#                 which the filter will be applied.
#
# output_file   : Elegant formatted sdds file that
#                 is the result of the filter.
#
# NOTE: output_file must be unique from input_file.
#
##################################################

# usage
if ! ( [ $1 ] ); then
    echo "usage:"
    echo "addt.sh input_file output_file"
    exit 1
fi

input=$1
output=$2

# get values for pCentral +/- 10%
pC=`sddsprintout $input -par=pCentral | awk '/pCentral/ {print $4}'`
pC_low=`rpnl $pC 0.95 mult`
pC_high=`rpnl $pC 1.05 mult`

# first filter by momentum:
# pCentral-10% < p < pCentral+10%
# then filter by time and momentum->
# remove particles outside of 10 std. dev.
sddsoutlier $input -pipe=out -noWarnings \
    -columns=p \
    -minimumLimit=$pC_low \
    -maximumLimit=$pC_high \
    | sddsoutlier -pipe -noWarnings \
    -columns=t,p -stDevLimit=10.0 \
    | sddsprocess -pipe -noWarning \
    -redefine=parameter,Particles,n_rows,type=long \
    | sddsprocess -pipe=in $output -noWarning \
    "-redefine=parameter,Charge,Cperpart Particles mult"

# clean up
if [ -e $input~ ]; then
    rm $input~
fi
