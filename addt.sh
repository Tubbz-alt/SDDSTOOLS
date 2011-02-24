#!/bin/sh
# \
exec tclsh "$0" "$@"

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
#                 simulation.
#
# reference_file: Elegant formatted sdds file that
#                 was used as the input for a
#                 Shower simulation.
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

set usage {usage: shower2elegant <modified_file> <reference_file>}
if {[llength $argv]!=2} {
    return -code error "$usage (1)"
}
set mod [lindex $argv 0]
set ref [lindex $argv 1]
if ![file exists $mod] {
	return -code error "not found: $mod"
}
if ![file exists $ref] {
	return -code error "not found: $ref"
}

if [file exists tmp.out] {exec rm tmp.out}

# create a temporary file where the particleID has been reassigned
# to be synonymous with the row number of the particle entry
exec sddsprocess $ref tmp.out -noWarning \
    "-redefine=column,particleID,i_row,type=long"

# assign the time variable to be equal to that of its ancestor
# particle from the input file fed into Shower
# (here particleID corresponds to the ancestor particle's row number)
exec sddsxref $mod tmp.out -noWarning \
    -equate=particleID -reuse=rows -take=t \
    -transfer=parameter,pCentral

# add the time of taversal from Shower to the initial time
exec sddsprocess -noWarning $mod \
    "-redefine=column,t,t deltat +,units=s"

if [file exists tmp.out] {exec rm tmp.out}
