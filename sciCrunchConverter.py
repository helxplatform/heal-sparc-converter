#!/usr/bin/env python3
import argparse
import sys
import json
import xml.etree.ElementTree as ET

def main(args):

    print (args.inputFile)
    json_blob = scicrunch_raw_to_json(args.inputFile)

    for dataset in json_blob:
        # Transform to dbGaP XML
        dataset_xml = json_to_dbgap_xml(dataset)
        # Format XML
        ET.indent(dataset_xml)
        # Write xml
        study_id = dataset['study_id'].replace("/","-")
        filename = f"{args.outputDir}/{study_id}.xml"
        dataset_xml.write(filename)

def scicrunch_raw_to_json(inputFile):
    '''
    Transforms the downloaded scicrunch data for a single collection (initially SPARK 
    with multiple datasets) and returns a single JSON blob of roughly the following format:

    [
        {  One of these for every dataset in the file
            "study_id": ,     from hits[i]._id
            "dataset_id": ,   from hits[i]._id
            "dataset_name": , from hits[i].name
            "variables": [
                {
                    "variable_id": ,   dataset_id.v1
                    "variable_name": , from the organ, species and keyword fields
                    "variable_description": none
                },
            ]
        },
        ...
    ]
    '''       
    hitDict = []
    json_blob = []

    with open(inputFile, "r") as fileToRead:
       inputJson = json.load(fileToRead)
       hitDict = inputJson["hits"]

    hitList = hitDict["hits"]
    for i in range(len(hitList)):
       print (hitList[i]["_id"])
       dataset = {}

       # First set up the dataset metadata
       dataset['study_id'] = hitList[i]["_id"]
       dataset['dataset_id'] = hitList[i]["_id"]
       try:
          dataset['dataset_name'] = hitList[i]["_source"]["item"]["name"]
       except KeyError:
          print("No name in this dataset")

       
       # Now for the variables
       dataset['variables'] = []
       
       # The variable data we want is in 3 places: 1) an array of keywords, 2) the organ field
       # and 3) the species field
       # The keywords
       try:
          for j in range(len(hitList[i]["_source"]["item"]["keywords"])):
             variable = {}
             variable['variable_id'] = hitList[i]["_id"] + ".v" + str(j + 1)
             print (hitList[i]["_source"]["item"]["keywords"][j]["keyword"])
             variable['variable_name'] = hitList[i]["_source"]["item"]["keywords"][j]["keyword"]
             variable['variable_description'] = ""
             dataset['variables'].append(variable)
       except KeyError:   
          print("No keywords in this dataset")

       
       # The organ
       try:
          variable = {}
          j = j + 1
          variable['variable_id'] = hitList[i]["_id"] + ".v" + str(j + 1)
          variable['variable_name'] = hitList[i]["_source"]["anatomy"]["organ"][0]["curie"]
          variable['variable_description'] = ""
          dataset['variables'].append(variable)

       except KeyError:
          print("No organ in this dataset")

       # The species
       try:
          variable = {}
          j = j + 1
          variable['variable_id'] = hitList[i]["_id"] + ".v" + str(j + 1)
          variable['variable_name'] = hitList[i]["_source"]["organisms"]["subject"][0]["species"]["curie"]
          variable['variable_description'] = ""
          dataset['variables'].append(variable)

       except KeyError:
          print("No species in this dataset")

       print (dataset)
       # Append dataset
       json_blob.append(dataset)

    return json_blob


def json_to_dbgap_xml(dataset):
    '''
    Transforms the JSON blob into a dbGaP XML format, e.g.:

    <data_table id="pht000700.v1" study_id="phs000166.v2" participant_set="1" 
    date_created="Thu Sep  3 15:21:50 2009">

    <variable id="phv00070931.v1">
        <name>SUBJ_ID</name>
        <description>Deidentified Subject ID</description>
        <type>integer</type>
    </variable>
    '''
    # Build root
    root = ET.Element("data_table")
    root.set("id",dataset["dataset_id"])
    root.set("study_id",dataset["study_id"])

    # Loop over each variable
    for var_dict in dataset['variables']:
        variable = ET.SubElement(root,"variable")
        variable.set("id",var_dict['variable_id'])
        name = ET.SubElement(variable, "name")
        name.text = var_dict.get('variable_name',"")
        desc = ET.SubElement(variable, "description")
        desc.text = var_dict.get('variable_description',"")

    return(ET.ElementTree(root))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transform SciCrunch download to dbGaP XML format")
    parser.add_argument('--inputFile',  action="store", help= "Specify the file to convert")
    parser.add_argument('--outputDir',  action="store", help ="Specify absolute path for outputs")

    args = parser.parse_args()

    main(args)
