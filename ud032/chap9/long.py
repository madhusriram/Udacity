#!/usr/bin/env python
"""
Which Region in India has the largest number of cities with longitude between
75 and 80?
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
                    "$match" : {"country": "India", "lon" : {"$gte" : 75, "$lte" : 80}}
                },
                {
                    "$unwind" : "$isPartOf"
                },
                {
                    "$group" : { "_id" : "$isPartOf", "count" : {"$sum" : 1}}   
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
    # The following statements will be used to test your code by the grader.
    # Any modifications to the code past this point will not be reflected by
    # the Test Run.
    db = get_db('examples')
    pipeline = make_pipeline()
    result = aggregate(db, pipeline)
    import pprint
    pprint.pprint(result[0])
    assert len(result) == 1
    assert result[0]["_id"] == 'Tamil Nadu'
    assert result[0]["count"] == 424

