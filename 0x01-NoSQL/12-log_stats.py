#!/usr/bin/env python3
""" Log stats """


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient("mongodb://127.0.0.1:27017")

    db = client.logs.nginx

    print("{} logs".format(db.count_documents({})))
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    for method in methods:
        print("\tmethod {}: {}".format(method, db.count_documents({"method": method})))

    print("{} status check".format(db.count_documents({"method": "GET", "path": "/status"})))
