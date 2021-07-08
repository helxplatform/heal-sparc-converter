#####################################################
#
# A container for processing the sparc data download
#
######################################################
FROM python:3.8.5-slim

# Create some needed local directories
RUN mkdir -p /usr/share/man/man1
RUN mkdir -p /usr/local/renci/bin
RUN mkdir -p /usr/local/renci/data

# Install required packages
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk wget && \
    cd /usr/local && \
    wget https://apache.claz.org/jena/binaries/apache-jena-4.1.0.tar.gz && \
    tar xvfz apache-jena-4.1.0.tar.gz && \
    pip3 install kgx && \
    rm -rf /var/cache/apk/*

# Move some local executables into the bin directory
ADD process_kgx.py /usr/local/renci/bin
ADD process_input.sh /usr/local/renci/bin

# Call process_input.sh with the 2 user provided input and output files
ENTRYPOINT ["/usr/local/renci/bin/process_input.sh"]
CMD ["inputFile", "outputFile"]
