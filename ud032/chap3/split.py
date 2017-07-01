"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in the range as described above,
  write that line to the output_good file
- if the value of the field is not a valid year as described above, 
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the 
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import re
import csv
import pprint
import datetime

INPUT_FILE = 'autos.csv'
OUTPUT_GOOD = 'autos-valid.csv'
OUTPUT_BAD = 'FIXME-autos.csv'

def is_valid_year(date_string):
    '''
    Check if it is a valid year and in the range 1886 to 2014 inclusive
    '''
    date_re = re.compile(r'^\d{4}')
    year = 0 
    if date_string:
        match = re.search(date_re, date_string)
        if match:
            year = int(match.group(0))
            if year >= 1886 and year <= 2014:
                return year
    return -1
 
def process_file(input_file, output_good, output_bad):
    '''
    
    '''
    goodrows = []
    badrows = []
    updaterows = []

    uri_re = re.compile(r'^http://dbpedia.org')

    with open(input_file, "r") as f:
        reader = csv.DictReader(f)
        header = reader.fieldnames
        for row in reader:
            if re.search(uri_re, row['URI']):
                updaterows.append(row)
            year = is_valid_year(row['productionStartYear'])
            if year != -1:
                row['productionStartYear'] = year
                goodrows.append(row)                            
            else:
                badrows.append(row)
     
    with open(output_good, "w") as g:
        writer = csv.DictWriter(g, delimiter=",", fieldnames= header)
        writer.writeheader()
        writer.writerows(goodrows)

    with open(output_bad, "w") as f:
        writer = csv.DictWriter(f, delimiter=",", fieldnames=header)
        writer.writeheader()
        writer.writerows(badrows)

    with open(input_file, "w") as f:
        writer = csv.DictWriter(f, delimiter=",", fieldnames=header)
        writer.writeheader()
        writer.writerows(updaterows)

def test():
    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)

if __name__ == "__main__":
    test()
