#!/bin/sh

#---------------------------------------------------
# Read sdds parameter file into plain data file.
# usage:
# $ readpar.sh input.par output.dat
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
    echo "read_par.sh input.par [output.dat]"
    exit 1
fi

# define variables from arguments
input=$1

if [ $2 ]; then
    output=$2
else
    output=${input%.par}
    output=$output.dat
fi

# don't overwrite existing output file
if [ -e $output ]; then
    echo "Error: output file $output aleardy exists."
    exit 1
fi

# generate plain text file from parameter file
sdds2plaindata $input $output \
-col=ElementName -col=ElementParameter \
-col=ParameterValueString -col=ParameterMode \
"-separator= " -noRowCount