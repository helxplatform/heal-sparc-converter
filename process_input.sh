#! /bin/bash
# we are expecting a .ttl file as input.  Otherwise it won't work ...
# maybe at some point we should do the wget for the input file in here. Something to consider
#
# This script is written to be used in a docker container.  The data directory containing the
# input and outputs should be mapped in.

# Example invocation: 
#
# docker run -v $PWD:/usr/local/renci/data testsparc curation-export.ttl curation-export-processed.json

# The input and output files
echo $1
echo $2

OUTFILEBASE=`basename $2`
FILEBASE=`basename $1 .ttl`

# This is local to the container
BASEDIR="/usr/local/renci/data"

# This directory is mapped in
EXECDIR="/usr/local/renci/bin"

# Run jena riot to convert the ttl file to nTriples format
/usr/local/apache-jena-4.1.0/bin/riot --output=nt ${BASEDIR}/$1 > ${BASEDIR}/${FILEBASE}.nt

# use kgx to convert nTriples to the kgx json format
kgx transform --input-format nt --output ${BASEDIR}/${FILEBASE}.json --output-format json ${BASEDIR}/${FILEBASE}.nt > ${BASEDIR}/kgx.log 2>&1

# This step converts the predicates that are uri's to predicates that Roger can load
# We are expecting this to evolve over time as our understanding of the Sparc data improves.
python3 $EXECDIR/process_kgx.py -i ${BASEDIR}/${FILEBASE}.json -o ${BASEDIR}/${OUTFILEBASE}
