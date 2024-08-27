#!/usr/bin/env python3
""" Update a document in Python """

def update_topics(mongo_collection, name, topics):
    """ changes all topics of a school document based on the name """
    return mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
