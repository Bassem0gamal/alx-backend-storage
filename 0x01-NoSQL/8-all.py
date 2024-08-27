#!/usr/bin/env python3
""" List all documents in Python """


def list_all(mongo_collection):
    """ lists all documents in a collection """
    return list(mongo_collection.find())
