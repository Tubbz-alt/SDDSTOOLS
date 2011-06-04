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

# Create new column 'Particle' which matches daughter
# particles to parent particles:
# ('i_row' of parent = 'Particle' of daughter)
sddsprocess $ref -noWarning \
    "-define=column,Particle,i_row,type=long" \
    "-define=parameter,Cperpart,Charge n_rows /,type=double"

# Take time variable 't' from parent particle and
# add 'deltat' (time to traverse Shower geometry).
# Also transfer 'pCentral' from reference file,
# and define parameters 'Particles' and 'Charge'.
sddsxref $mod $ref -noWarning \
    -equate=Particle -reuse=rows -take=t,particleID \
    -transfer=parameter,pCentral \
    -transfer=parameter,Cperpart
sddsprocess $mod -noWarning \
    "-redefine=column,t,t deltat +,units=s" \
    "-define=parameter,Particles,n_rows,type=long" \
    "-define=parameter,Charge,Cperpart Particles *,type=double"

# clean up
rm $mod~

# return reference file to original state
mv $ref~ $ref
