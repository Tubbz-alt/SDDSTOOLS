#!/bin/sh  
# \
exec tclsh "$0" "$@"

##################################################
#
# ele2show.sh
# ===========
#
# Converts Shower formatted sdds file into
# Elegant formatted sdds file.
#
# ------------------------------------------------
#
# Usage
# =====
#
# show2ele.sh shower_file elegant_file
#
# ------------------------------------------------
#
# Arguments
# =========
#
# shower_file  : Shower formatted sdds file to be
#                converted to Elegant format.
#
# elegant_file : Name of new Elegant formatted sdds
#                file.
#
##################################################

proc APSStrictParseArguments {optlist} {
    upvar args arguments
    set length [llength $arguments]
    set index 0
    set leftovers {}
    while {$index<$length} {
        set arg [lindex $arguments $index]
        if {[string index $arg 0]=="-"} {
            set keywordName [string range $arg 1 end]
            if {[lsearch -exact $optlist $keywordName]!=-1} {
                incr index
                if {$index==$length} {
                    lappend leftovers $arg
                } else {
                    set valueString [lindex $arguments $index]
                    uplevel "set $keywordName {$valueString}"
                    incr index
                }
            } else {
                incr index
                lappend leftovers $arg
            }
        } else {
            lappend leftovers $arg
            incr index
        }
    }
    set arguments [concat $leftovers]
    if {$arguments != ""} {
        set procName [lindex [info level [expr {[info level] - 1}]] 0]
        puts stderr "Unknown option(s) given to $procName \"$arguments\""
        return -1
    } else {
        return 0
    }
}

set usage {usage: shower2elegant.sh <input> <output> [-positrons 1] [-reference "x y u v"]}
if {[llength $argv]!=2 && [llength $argv]!=4} {
    return -code error "$usage (1)"
}
set input  [lindex $argv 0]
set output [lindex $argv 1]
if ![file exists $input] {
    return -code error "not found: $input"
}
if [file exists $output] {
    return -code error "exists: $output"
}

set reference "0 0 0 0"
set positrons 0
set args [lrange $argv 2 end]
if {[APSStrictParseArguments {reference positrons}]} {
	return -code error "$usage (2)"
}
set xref [lindex [split $reference] 0]
set yref [lindex [split $reference] 1]
set uref [lindex [split $reference] 2]
set vref [lindex [split $reference] 3]

set type electrons
if $positrons {
    set type positrons
} 

# NOTE: Adds new column 'deltat', which represents the
#       time of traversal across the geometry used in
#       the shower simulation.
exec sddsprocess $input -pipe=out \
    -match=parameter,Type=$type \
    -filter=column,w,0.01,1.01 \
    "-define=column,xp,u $uref - w /" \
    "-define=column,yp,v $vref - w /" \
    "-define=column,p,Energy mev / sqr 1 - sqrt" \
    "-define=column,vz,w c_mks *,units=m/s" \
    "-process=z,average,deltaz" \
    "-define=column,deltat,deltaz vz /,units=s" \
    -redefine=column,particleID,Particle,type=long \
    | sddsconvert -pipe -retain=column,x,y,xp,yp,p,deltat,particleID \
    -retain=parameter,deltaz \
    | sddscombine -pipe=in $output -merge
