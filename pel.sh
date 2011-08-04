#!/bin/bash
bsub -N -u fc49ca.1284327@push.boxcar.io -a mympi -q beamphysics -n 2 -o run.log Pelegant $1
