#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Please note that the function 'make_request' is provided for your reference only.
# You will not be able to to actually use it from within the Udacity web UI.
# Your task is to process the HTML using BeautifulSoup, extract the hidden
# form field values for "__EVENTVALIDATION" and "__VIEWSTATE" and set the appropriate
# values in the data dictionary.
# All your changes should be in the 'extract_data' function
from bs4 import BeautifulSoup
import requests
import json

html_page = "page_source.html"

def extract_data(page):
    data = {"eventvalidation": "",
            "viewstate": ""}
    with open(page, "r") as html:
        soup = BeautifulSoup( html, 'html.parser')
        form = soup.find_all('form', attrs={"name":"form1"})
        data['viewstate'] = form[0].find_all('input', attrs={"name":"__VIEWSTATE"})[0].get('value')
        data['eventvalidation'] = form[0].find_all('input', attrs={"name":"__EVENTVALIDATION"})[0].get('value')
    return data


def make_request(data):
    eventvalidation = data["eventvalidation"]
    viewstate = data["viewstate"]

    r = requests.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate
                    })

    return r.text


def test():
    data = extract_data(html_page)
    assert data["eventvalidation"] != ""
    assert data["eventvalidation"].startswith("/wEWjAkCoIj1ng0")
    assert data["viewstate"].startswith("/wEPDwUKLTI")

    
test()
