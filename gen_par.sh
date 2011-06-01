#!/bin/sh

#---------------------------------------------------
# Generate sdds parameter file from plain data file.
# usage:
# $ genpar.sh input.dat output.par
#
# Format of plain data file:
#
# name parameter value mode
# 
# NOTE: 'value' column can contain double or string.
#---------------------------------------------------

plaindata2sdds $1 $2 \
-col=ElementName,string -col=ElementParameter,string \
-col=ParameterValueString,string -col=ParameterMode,string \
-noRowCount -outputMode=binary
