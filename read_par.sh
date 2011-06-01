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

sdds2plaindata $1 $2 \
-col=ElementName -col=ElementParameter \
-col=ParameterValueString -col=ParameterMode \
"-separator= " -noRowCount