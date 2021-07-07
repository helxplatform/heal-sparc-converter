# heal-sparc-converter
This directory produces a docker container that converts the curation-export.ttl data download from the Sparc project to a kgx formatted json file that can be loaded by roger. The file is downloaded from

https://cassava.ucsd.edu/sparc//exports/

The .ttl file is converted to nTriples format using the riot tool from Apache Jena.  The nTriples file is convert to kgx formatted json using the kgx transform command.  Finally, some of the predicates are replaced with UBERON equivalents using process_kgx.py

Example command line:

docker run -v $PWD:/usr/local/renci/data testsparc curation-export.ttl curation-export-processed.json

where the mapped directory contains the local copies of the input, output and kgx log files.
