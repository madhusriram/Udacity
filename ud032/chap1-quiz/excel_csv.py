# -*- coding: utf-8 -*-
'''
Find the time and value of max load for each of the regions
COAST, EAST, FAR_WEST, NORTH, NORTH_C, SOUTHERN, SOUTH_C, WEST
and write the result out in a csv file, using pipe character | as the delimiter.

An example output can be seen in the "example.csv" file.
'''

import xlrd
import os
import csv
from zipfile import ZipFile

datafile = "2013_ERCOT_Hourly_Load_Data.xls"
outfile = "2013_Max_Loads.csv"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall()


def parse_file(datafile):
    '''
    This function will convert the .xls to .csv
    '''
    data = []
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = [[sheet.cell_value(row, col) for col in range(sheet.ncols)] for row in range(sheet.nrows)]
    for i in range(1, sheet.nrows):
        data[i][0] = xlrd.xldate_as_tuple(data[i][0], 0)
    return data

def get_max_load(data, index):
    '''
    '''
    return max(data, key=lambda x: x[index])

def save_file(data, filename):
    '''
    write the data in list format to the CSV
    '''

    with open(filename, 'wb') as csvfile:
        header = ['Station', 'Year', 'Month', 'Day', 'Hour', 'Max Load']
        csvfile = csv.writer(csvfile, delimiter='|')
        csvfile.writerow(header)
        for i in range(1, len(data[1])):
            row = get_max_load(data[1:], i)
            if data[0][i] == 'ERCOT':
                continue
            row_elements = [data[0][i], row[0][0], row[0][1], row[0][2], row[0][3], row[i]]
            csvfile.writerow(row_elements)
             
def test():
    open_zip(datafile)
    data = parse_file(datafile)
    save_file(data, outfile)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(outfile) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8

        # Check Station Names
        assert set(stations) == set(correct_stations)
        
if __name__ == "__main__":
    test()
