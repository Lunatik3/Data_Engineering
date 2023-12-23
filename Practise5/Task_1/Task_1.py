import json
import msgpack
from pymongo import MongoClient


def connect():
    client = MongoClient()
    db = client["database_1"]
    return db.person


def read_file(filename):
    with open(filename, 'rb') as file:
        content = file.read()
        data = msgpack.unpackb(content)
    #print(data)
    return data

#data = read_file("task_1_item.msgpack")

def insert_many(collection, data):
    collection.insert_many(data)


def sort_by_salary(collection):
    items = []
    for person in collection.find({}, limit=10).sort({'salary': -1}):
        person.pop('_id')
        items.append(person)
        # print(person)
    return items


def filter_by_age(collection):
    items = []
    for person in (collection.find({"age": {"$lt": 30}}, limit=15).sort({"salary": -1})):
        person.pop('_id')
        items.append(person)
        #print(person)
    return items


def filter_by_city_and_job(collection):
    items = []
    for person in (collection.find({"city": "Хихон",
                   "job": {"$in": ["Врач", "Косметолог", 'Психолог']}},limit=10).sort({"age": 1})):
        person.pop('_id')
        items.append(person)
        #print(person)
    return items


def age_year(collection):
    items = []
    result = collection.count_documents({
        "age": {"$gt": 25, "$lt": 35},
        "year": {"$gte": 2019, "$lte": 2022},
        "$or": [
            {"salary": {"$gt": 50000, "$lte": 75000}},
            {"salary": {"$gt": 125000, "$lt": 150000}}
        ]
    })
    items.append({'count': result})
    return items



with open("salary_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(sort_by_salary(connect()), ensure_ascii=False))

with open("age_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(filter_by_age(connect()), ensure_ascii=False))

with open("city_and_job_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(filter_by_city_and_job(connect()), ensure_ascii=False))

with open("age_year_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(age_year(connect()), ensure_ascii=False))

# insert_many(connect(), data)
