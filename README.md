# heal-sparc-converter
This directory produces a docker container that converts the curation-export.ttl data download from the Sparc project to a kgx formatted json file that can be loaded by roger. The file is downloaded from

https://cassava.ucsd.edu/sparc//exports/

The .ttl file is converted to nTriples format using the riot tool from Apache Jena.  The nTriples file is convert to kgx formatted json using the kgx transform command.  Finally, some of the predicates are replaced with UBERON equivalents using process_kgx.py

Example command line:

docker run -v $PWD:/usr/local/renci/data testsparc curation-export.ttl curation-export-processed.json

where the mapped directory contains the local copies of the input, output and kgx log files.


# getting the data from scicrunch
To use the SciCrunch API you need an api key. In order to get API key:

1) Create an account at https://scicrunch.org

2) Create an API key - Select 'API Keys' from ‘MY ACCOUNT’ and that will take you to the page to generate an API key

3) With the API key you can now access the ElasticSearch endpoint

You then retrieve the data using the scicrunch API: Here's an example including a redacted API key:

curl 'https://scicrunch.org/api/1/elastic/SPARC_PortalDatasets_pr/_search?api_key=YOUR_API_KEY&size=150'

Note the size paramater at the end: it specifies the number of records to retrieve.  150 is currrently enough to retrieve the entire dataset, but that number may have to increase in the future

Once you have saved the data to a file

The next step is to run the code sciCrunchConverter.py This code takes 2 arguments which are the downloaded file and the directory for the outputs.

Example usage:
	./sciCrunchConverter.py --inputFile SciCrunchSparc-27-09-2021.json --outputDir outputs

The data is transformed into db_gap XML files, one for each dataset in the download. The transformation is according to the following:

        {  One of these for every dataset in the file
            "study_id": ,     from hits[i]._id
            "dataset_id": ,   from hits[i]._id
            "dataset_name": , from hits[i].name
            "variables": [
                {
                    "variable_id": ,   dataset_id.v1
                    "variable_name": , from the organ, species and keyword fields
                    "variable_description": same as the variable_name
                },
            ]
        }

