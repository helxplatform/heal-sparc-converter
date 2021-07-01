import argparse
import json


def get_file_contents(file_path):
    """Read kgx file"""
    with open(file_path) as f:
        return json.load(f)


def write_kgx_out(out_file_path, kgx_data):
    """ Write kgx file"""
    with open(out_file_path, 'w') as f:
        json.dump(kgx_data, f, indent=2)


def map_predicates(edges):
    """
    Maps predicate attribute of edges to biolink type
    if no mapping is found predicate `biolink:related_to` is used
    """
    # @TODO maybe these need to be more specific
    mapping = {
        ':http://uri.interlex.org/temp/uris/aboutContributor': 'biolink:contributor',
        ':http://uri.interlex.org/temp/uris/aboutDataset': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/asBaseUnits': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/contributorTo': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/dereferencesTo': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasAffiliation': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasAge': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasAwardNumber': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasContactPerson': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasDerivedInformationAsParticipant': ' biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasDoi': 'biolink:publications',
        ':http://uri.interlex.org/temp/uris/hasHumanUri': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasProtocol': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasResponsiblePrincipalInvestigator': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasRole': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasUnit': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/hasUriApi': 'biolink:xref',
        ':http://uri.interlex.org/temp/uris/hasUriHuman': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/involvesAnatomicalRegion': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/isAboutParticipant': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/isDescribedBy': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/protocolEmploysTechnique': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/subjectHasHeight': 'biolink:related_to',
        ':http://uri.interlex.org/temp/uris/wasDerivedFromSubject': 'biolink:related_to',
        ':http://uri.interlex.org/tgbugs/uris/readable/hasAnnotation': 'biolink:related_to',
        ':http://uri.interlex.org/tgbugs/uris/readable/sparc/animalSubjectHasWeight': 'biolink:related_to',
        ':http://uri.interlex.org/tgbugs/uris/readable/sparc/hasORCIDId': 'biolink:related_to',
        ':http://uri.interlex.org/tgbugs/uris/readable/sparc/specimenHasIdentifier': 'biolink:related_to',
        'biolink:author': 'biolink:author',
        'biolink:related_to': 'biolink:related_to',
        'biolink:same_as': 'biolink:related_to',
        'owl:imports': 'biolink:related_to',
        'owl:onDatatype': 'biolink:related_to',
        'owl:versionIRI': 'biolink:related_to',
        'owl:withRestrictions': 'biolink:related_to',
        'rdf:first': 'biolink:related_to',
        'rdf:rest': 'biolink:related_to'
    }
    for e in edges:
        e['predicate'] = mapping.get(e['predicate'], 'biolink:related_to')
    return edges


def add_ids(edges):
    """
    Adds ids to edges missing ids
    """
    for e in edges:
        if 'id' not in e:
            e['id'] = e['subject'] + '-' + e['predicate'] + '-' + e['object']
    return edges

def main(input, output):
    kgx = get_file_contents(input)
    print('adding ids to edges')
    kgx['edges'] = add_ids(kgx['edges'])
    print('mapping predicates')
    kgx['edges'] = map_predicates(kgx['edges'])
    print('writing out file')
    write_kgx_out(kgx_data=kgx, out_file_path=output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KGX correction tool for spac dataset')
    parser.add_argument('-i', '--input-file', help='input file name')
    parser.add_argument('-o', '--output-file', help='output file name')
    args = parser.parse_args()
    input_file_name = args.input_file
    output_file_name = args.output_file
    main(input_file_name, output_file_name)