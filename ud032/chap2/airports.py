#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete the 'extract_airports()' function so that it returns a list of airport
codes, excluding any combinations like "All".

Refer to the 'options.html' file in the tab above for a stripped down version
of what is actually on the website. The test() assertions are based on the
given file.
"""

from bs4 import BeautifulSoup
html_page = "options.html"

import re

pattern = re.compile(r'^all', re.IGNORECASE)

def extract_airports(page):
    data = []
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "html.parser")
        airportlist = soup.find_all('select', attrs={'id':'AirportList'})
        for opt in airportlist[0].find_all('option'):
            airport_codes = opt.get('value')
            if not re.search(pattern, airport_codes):
                data.append(airport_codes)
    return data


def test():
    data = extract_airports(html_page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data

if __name__ == "__main__":
    test()
