#!/bin/sh

#---------------------------------------------------
# Generate sdds parameter file from plain data file.
# usage:
# $ genpar.sh input.dat [output.par]
#
# Format of plain data file:
#
# name parameter value mode
# 
# NOTE: 'value' column can contain double or string.
#---------------------------------------------------

# usage
if ! [ $1 ]; then
    echo "usage:"
    echo "gen_par.sh input.dat [output.par]"
    exit 1
fi

# define variables from arguments
input=$1

if [ $2 ]; then
    output=$2
else
    output=${input%.dat}
    output=$output.par
fi

# don't overwrite existing output file
if [ -e $output ]; then
    echo "Error: output file $output aleardy exists."
    exit 1
fi

# generate parameter file from plain text file
plaindata2sdds $input $output \
-col=ElementName,string -col=ElementParameter,string \
-col=ParameterValueString,string -col=ParameterMode,string \
-noRowCount -outputMode=binary
