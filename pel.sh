#!/bin/bash
bsub -a mympi -q beamphysics -n 2 -o run.log Pelegant $1
