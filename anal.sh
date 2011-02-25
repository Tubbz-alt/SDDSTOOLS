#!/bin/sh

###########################################
#
# anal.sh
#
# Applies sddsanalyzebeam to an SDDS file.
#
# -----------------------------------------
#
# Usage
# =====
#
# anal.sh data.sdds [data.ana]
#
# -----------------------------------------
#
# Arguments
# =========
#
# data.sdds : SDDS file to be analyzed.
#             If the file's extension is
#             either '.sdds', or '.out',
#             it may be omitted.
#
# data.ana  : Name of outputfile. If not
#             specified, will be the base
#             name of the input file with
#             the extension '.ana'.
#
###########################################

# usage
if ! [ $1 ]; then
    echo "usage:"
    echo "anal.sh data.sdds [data.ana]"
    exit 1
fi

# define variables from arguments
data_base=${1%.*}
ana=$2

# get full data file name
if [ "$1" == "$data_base" ];then
    if [ -e $data_base.out ]; then
	data=$data_base.out
    fi
    if [ -e $data_base.sdds ]; then
	data=$data_base.sdds
    fi
fi

if [ $ana ]; then
    sddsanalyzebeam $data $ana
else
    sddsanalyzebeam $data $data_base.ana
fi
