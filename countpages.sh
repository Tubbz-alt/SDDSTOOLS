#!/bin/sh

#============================================================
# countpages.sh
#
# Routine to print the number of pages in an sdds file.
#
# How it works:
#
# 1) Collapse the input file into a new file where each row
# contains the parameters of a single page of the input file.
#
# 2) Define a new parameter in the new file that is simply
# the number of rows in the new file, which is also the
# number of pages in the input file.
#
# 3) Print the page count of the input file to the screen.
#
# Usage:
# $ countpages.sh input.sdds
#
#============================================================

sddscollapse $1 -pipe=out -noWarning |\
    sddsprocess -pipe -noWarnings \
    "-define=parameter,pagecount,n_rows,type=long" |\
    sddsprintout -pipe=in -par=pagecount |\
    awk '/pagecount/ {print $3}'
