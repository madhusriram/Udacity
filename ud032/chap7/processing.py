#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
In this problem set you work with another type of infobox data, audit it,
clean it, come up with a data model, insert it into MongoDB and then run some
queries against your database. The set contains data about Arachnid class
animals.

Your task in this exercise is to parse the file, process only the fields that
are listed in the FIELDS dictionary as keys, and return a list of dictionaries
of cleaned values. 

The following things should be done:
- keys of the dictionary changed according to the mapping in FIELDS dictionary
- trim out redundant description in parenthesis from the 'rdf-schema#label'
  field, like "(spider)"
- if 'name' is "NULL" or contains non-alphanumeric characters, set it to the
  same value as 'label'.
- if a value of a field is "NULL", convert it to None
- if there is a value in 'synonym', it should be converted to an array (list)
  by stripping the "{}" characters and splitting the string on "|". Rest of the
  cleanup is up to you, e.g. removing "*" prefixes etc. If there is a singular
  synonym, the value should still be formatted in a list.
- strip leading and ending whitespace from all fields, if there is any
- the output structure should be as follows:

[ { 'label': 'Argiope',
    'uri': 'http://dbpedia.org/resource/Argiope_(spider)',
    'description': 'The genus Argiope includes rather large and spectacular spiders that often ...',
    'name': 'Argiope',
    'synonym': ["One", "Two"],
    'classification': {
                      'family': 'Orb-weaver spider',
                      'class': 'Arachnid',
                      'phylum': 'Arthropod',
                      'order': 'Spider',
                      'kingdom': 'Animal',
                      'genus': None
                      }
  },
  { 'label': ... , }, ...
]

  * Note that the value associated with the classification key is a dictionary
    with taxonomic labels.
"""
import codecs
import csv
import json
import pprint
import re

DATAFILE = 'arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}

def isnull(val):
    '''
    return None if field is NULL, else strip leading and trailing white spaces 
    and return
    '''
    if val == 'NULL':
        return None
    
    return val.rstrip()

def parse_synonym(string):
    '''
    parse the synonym value which can be a list of values into a string and return
    '''
    if string == 'NULL':
        return None
    if string[0] == '{' and string[-1] == '}':
        string = string.lstrip('{').rstrip('}')
        arr = string.split('|')
        arr = [i.strip() for i in arr]
        return arr
    return [string.strip()]

def process_file(filename, fields):

    process_fields = fields.keys()
    
    data = []
    
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for i in range(3):
            l = reader.next()

        for line in reader:
            new_dict = {}
            for key, val in fields.iteritems():
                # Populate the classification
                if 'classification' not in new_dict:
                    new_dict['classification'] = {}
                if val == 'class':
                    new_dict['classification']['class'] = isnull(line['class_label'])
                if val == 'family':
                    new_dict['classification']['family'] = isnull(line['family_label'])
                if val == 'kingdom':
                    new_dict['classification']['kingdom'] = isnull(line['kingdom_label'])
                if val == 'genus':    
                    new_dict['classification']['genus'] = isnull(line['genus_label'])
                if val == 'order':
                    new_dict['classification']['order'] = isnull(line['order_label'])
                if val == 'phylum':    
                    new_dict['classification']['phylum'] = isnull(line['phylum_label'])
                # Trim the label 
                if val == 'label':
                    m = re.search(r'(\w+)\s+\(\w+\)', line[key])
                    if m:
                        new_dict[val] = isnull(m.group(1))
                    else:
                        new_dict[val] = isnull(line[key])
                # Filter the name
                if val == 'name':
                    new_dict['name'] = isnull(line[key])
                # Process the synonym
                if val == 'synonym':
                    new_dict[val] = []
                    new_dict[val] = parse_synonym(line[key])
                # Process the URI
                if val == 'uri':
                    new_dict[val] = isnull(line[key])
                # Process the description
                if val == 'description':
                    new_dict[val] = isnull(line[key])
            if not new_dict['name'] or not re.search(r'[\w\s\d]+', new_dict['name']):
                new_dict['name'] = new_dict['label']
            data.append(new_dict)
    return data

def test():
    data = process_file(DATAFILE, FIELDS)
    print "Your first entry:"
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None, 
        "name": "Argiope", 
        "classification": {
            "kingdom": "Animal", 
            "family": "Orb-weaver spider", 
            "order": "Spider", 
            "phylum": "Arthropod", 
            "genus": None, 
            "class": "Arachnid"
        }, 
        "uri": "http://dbpedia.org/resource/Argiope_(spider)", 
        "label": "Argiope", 
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }
    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()
