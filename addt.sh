#!/bin/sh

##################################################
#
# addt.sh
# =======
#
# Adds temporal profile back into an sdds beam file
# after a Shower simulation.
#
# ------------------------------------------------
#
# Usage
# =====
#
# addt.sh modified_file reference_file
#
# ------------------------------------------------
#
# Arguments
# =========
#
# modified_file : Elegant formatted sdds file that
#                 was the result of a Shower
#                 simulation. Will be modified to
#                 add the proper time component
#                 to each particle.
#
# reference_file: Elegant formatted sdds file that
#                 was used as the input for a
#                 Shower simulation. Will be used
#                 as a reference file for setting
#                 the time component of the
#                 modified file.
#
##################################################

# usage
if ! ( [ $1 ] && [ $2 ] ); then
    echo "usage:"
    echo "addt.sh modified_file reference_file"
    exit 1
fi

# modified file:
# output of Shower;
# contains daughter particles
mod=$1

# reference file:
# input to Shower;
# contains parent particles
ref=$2

# Create new column 'tmpID' which matches daughter
# particles to parent particles:
# ('i_row' of parent = 'particleID' of daughter)
sddsprocess $ref -noWarning \
    "-define=column,tmpID,i_row,type=long"
sddsprocess $mod -noWarning \
    "-define=column,tmpID,particleID,type=long"

# Take time variable 't' from parent particle and
# add 'deltat' (time to traverse Shower geometry).
# Also transfer 'pCentral' and define 'Particles'.
sddsxref $mod $ref -noWarning \
    -equate=tmpID -reuse=rows -take=t \
    -transfer=parameter,pCentral
sddsprocess $mod -noWarning \
    "-define=parameter,Particles,n_rows,type=long" \
    "-redefine=column,t,t deltat +,units=s" \

# clean up
rm $mod~

# return reference file to original state
mv $ref~ $ref
