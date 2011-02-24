#!/bin/sh  
# \
exec tclsh "$0" "$@"

##################################################
#
# ele2show.sh
# ===========
#
# Converts Elegant formatted sdds file into
# Shower formatted sdds file.
#
# ------------------------------------------------
#
# Usage
# =====
#
# ele2show.sh elegant_file shower_file
#
# ------------------------------------------------
#
# Arguments
# =========
#
# elegant_file : Elegant formatted sdds file to be
#                converted to Shower format.
#
# shower_file  : Name of new Shower formatted sdds
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

set usage {usage: elegant2shower.sh <input> <output> [-reference "x y xp yp"]}
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
set args [lrange $argv 2 end]
if {[APSStrictParseArguments {reference}]} {
	return -code error "$usage (2)"
}
set xref [lindex [split $reference] 0]
set yref [lindex [split $reference] 1]
set xpref [lindex [split $reference] 2]
set ypref [lindex [split $reference] 3]

exec sddsprocess $input -pipe=out \
    "-define=column,w,xp sqr yp sqr + 1 + sqrt rec" \
    "-define=column,u,xp $xpref - w *" \
    "-define=column,v,yp $ypref - w *" \
    "-define=column,Energy,p sqr 1 + sqrt mev *,units=MeV" \
    "-define=column,z,0,units=m" \
    "-redefine=column,x,x $xref -,units=m" \
    "-redefine=column,y,y $yref -,units=m" \
    "-reprint=parameter,Type,electrons" \
    | sddsconvert -pipe=in $output -retain=column,u,v,w,x,y,z,Energy,t

