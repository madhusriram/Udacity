#!/usr/bin/env python
"""
For this exercise, let's return to our cities infobox dataset. The question we would like you to answer
is as follows:  Which region or district in India contains the most cities? (Make sure that the count of
cities is stored in a field named 'count'; see the assertions at the end of the script.)
{
    "_id" : ObjectId("52fe1d364b5ab856eea75ebc"),
    "elevation" : 1855,
    "name" : "Kud",
    "country" : "India",
    "lon" : 75.28,
    "lat" : 33.08,
    "isPartOf" : [
        "Jammu and Kashmir",
        "Udhampur district"
    ],
    "timeZone" : [
        "Indian Standard Time"
    ],
    "population" : 1140
}

One thing to note about the cities data is that the "isPartOf" field contains an array of regions or 
districts in which a given city is found. See the example document in Instructor Comments below.

"""

def get_db(db_name):
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [
                {
                    "$match" : { "country" : "India" }
                },
                {
                    "$unwind" : "$isPartOf"
                },
                {
                    "$group" : { "_id" : "$isPartOf", "count" : { "$sum" : 1 }}
                },
                {
                    "$sort" : { "count" : -1 }
                },
                {
                    "$limit" : 1
                }    
                ]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.cities.aggregate(pipeline)]

if __name__ == '__main__':
    db = get_db('examples')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    print "Printing the first result:"
    import pprint
    pprint.pprint(result[0])
    assert result[0]["_id"] == "Uttar Pradesh"
    assert result[0]["count"] == 623



