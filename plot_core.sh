#!/bin/sh

###########################################
#
# plot_core.sh
#
# Allows the user to plot the core of the
# beam when used in conjunction with one
# of the other plotting tools. Removes
# particles outside of specified rms factor
# equally in all phase space coordinates.
# In other words, the final plot shows
# only the particles contained within a
# 6-D hypercube with sides specified in
# units of sigma_rms.
#
# NOTE: This script does NOT alter the
# SDDS input file containing the data to
# be plotted. Therefore it is "safe".
#
# -----------------------------------------
#
# Usage
# =====
#
# plot_core.sh limit plot.sh data.sdds \
#   plot_arg1 plot_arg2 plot_arg3 (etc.)
#
# -----------------------------------------
#
# Arguments
# =========
#
# limit       : The limit used to define the
#               beam core in units of
#               sigma_rms. All particles that
#               are above this limit in any
#               phase space coordinate are
#               removed for the upstream
#               plotting process.
#
# plot.sh     : The plotting script to be used.
#
# data.sdds   : The SDDS file containing the
#               data to be plotted.
#               If the file's extension is
#               either '.sdds', or '.out',
#               it may be omitted.
#
# plot_arg[N] : The arguments to be given
#               to the plotting script.
#
#
# -----------------------------------------
#
# Example
# =======
#
# Example usage:
#
# plot_core.sh 5.0 plot_gauss.sh input.sdds x y
#
# This example will produce a plot of x vs.
# y drawn from the file 'input.sdds' that
# includes only the particles that satisfy
# the following conditions:
#
# |x|  < 5.0 * sigma_rms_x
# |xp| < 5.0 * sigma_rms_xp
# |y|  < 5.0 * sigma_rms_y
# |yp| < 5.0 * sigma_rms_yp
# |z|  < 5.0 * sigma_rms_z
# |d|  < 5.0 * sigma_rms_d
#
###########################################

# define variables from arguments
limit=$1
script=$2
data_base=${3%.*}
args=( $4 $5 $6 $7 $8 $9 ${10} ${11} ${12} ${13})

# get full data file name
if [ "$3" == "$data_base" ];then
    if [ -e $data_base.out ]; then
	data=$data_base.out
    fi
    if [ -e $data_base.sdds ]; then
	data=$data_base.sdds
    fi
else
    data=$1
fi

# clean up
if [ -e $data_base.core ]; then
    rm $data_base.core
fi

# define z & d columns
sddsprocess $data $data_base.core -noWarnings \
 "-process=t,average,tbar" \
 "-define=column,z,t tbar - 2.99792458E11 *,units=mm" \
 "-define=column,d,p pCentral - pCentral / 100 *,units=%"

# remove particles outside of limit
sddsoutlier $data_base.core -noWarnings \
    -columns=x,xp,y,yp,z,d -stDevLimit=$limit

# remove z & d columns
# (plotting script doesn't expect them)
sddsprocess $data_base.core -noWarnings \
 "-delete=parameter,tbar" \
 "-delete=column,z" \
 "-delete=column,d"

# call the plotting script
$script $data_base.core ${args[@]:0}

# clean up
if [ -e $data_base.core ]; then
    rm $data_base.core
fi
if [ -e $data_base.core~ ]; then
    rm $data_base.core~
fi
