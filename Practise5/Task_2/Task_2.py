import json
import csv

from pymongo import MongoClient


def connect():
    client = MongoClient()
    db = client["database_1"]
    return db.person

def read_file():
    data = []
    with open('task_2_item.csv', 'r', encoding="utf-8") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=';')
        for item in csv_reader:
            item['salary'] = int(item['salary'])
            item['id'] = int(item['id'])
            item['year'] = int(item['year'])
            item['age'] = int(item['age'])
            data.append(item)

    return data

def insert_many(collection):
    collection.insert_many(read_file())


def get_stat_by_salary(collection):
    items = []
    charact = [
        {"$group": {"_id": "result",
                    "max": {"$max": "$salary"},
                    "min": {"$min": "$salary"},
                    "avg": {"$avg": "$salary"}}}
    ]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_freq_by_job(collection):
    items = []
    charact = [{
        "$group": {
                    "_id": "$job",
                    "count": {"$sum": 1}
                   }
          },
        {
        "$sort": {"count": -1}
         }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_stat_salary_by_city(collection):
    items = []
    charact = [{
        "$group": {
            "_id": "$city",
            "max": {"$max": "$salary"},
            "min": {"$min": "$salary"},
            "avg": {"$avg": "$salary"}
                    }
            },
        {
            "$sort": {"avg": -1}
        }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_stat_salary_by_job(collection):
    items = []
    charact = [{
        "$group": {
            "_id": "$job",
            "max": {"$max": "$salary"},
            "min": {"$min": "$salary"},
            "avg": {"$avg": "$salary"}
        }
    },
        {
            "$sort": {"avg": -1}
        }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_stat_age_by_city(collection):
    items = []
    charact = [{
        "$group": {
            "_id": "$city",
            "max": {"$max": "$age"},
            "min": {"$min": "$age"},
            "avg": {"$avg": "$age"}
        }
    },
        {
            "$sort": {"avg": -1}
        }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_stat_age_by_job(collection):
    items = []
    charact = [{
        "$group": {
                   "_id": "$job",
                   "max": {"$max": "$age"},
                   "min": {"$min": "$age"},
                   "avg": {"$avg": "$age"}
        }
    },
        {
            "$sort": {"avg": -1}
        }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_max_salary_by_min_age(collection):
    items = []
    charact = [{
        "$group": {"_id": "age",
                   "age": {"$min": "$age"},
                   "max_salary": {"$max": "$salary"}}}, {
        "$match": {"age": 18}}
    ]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_min_salary_by_max_age(collection):
    items = []
    charact = [{
        "$group": {"_id": "age",
                   "age": {"$max": "$age"},
                   "min_salary": {"$min": "$salary"}}}, {
        "$match": {"age": 65}}
    ]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_50k_salary_by_avg_age(collection):
    items = []
    charact = [{
        "$match": {"salary": {"$gt": 50000}}}, {
        "$group": {"_id": "$city",
                   "max": {"$max": "$age"},
                   "min": {"$min": "$age"},
                   "avg": {"$avg": "$age"}}
            },
        {
            "$sort": {"avg": -1}
        }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_salary_by_city_job_age(collection):
    items = []
    charact = [{
        "$match": {
            "city": {"$in": ["Хихон", "Эльче", "Артейхо", "Сан-Себастьян"]},
            "job": {"$in": ["Косметолог", "Медсестра", "Оператор call-центра", "Инженер"]},
            "$or": [{"age": {"$gt": 18, "$lt": 25}},
                    {"age": {"$gt": 50, "$lt": 65}}]}},
        {
        "$group": {"_id": "res",
                   "max_salary": {"$max": "$salary"},
                   "min_salary": {"$min": "$salary"},
                   "avg_salary": {"$avg": "$salary"}}},
        {
        "$sort": {"count": -1}
         }]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

def get_salary_by_year_for_manager(collection):
    items = []
    charact = [{
        "$match": {
            "job": {"$in": ["Менеджер"]},}}, {
        "$group": {"_id": "$year",
                   "max": {"$max": "$salary"},
                   "min": {"$min": "$salary"},
                   "avg": {"$avg": "$salary"}}},{
        "$sort": {"min": -1}
    }

    ]
    for item in collection.aggregate(charact):
        items.append(item)
    return items

with open("get_stat_by_salary.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_stat_by_salary(connect()), ensure_ascii=False))

with open("get_freq_by_job.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_freq_by_job(connect()), ensure_ascii=False))

with open("get_stat_salary_by_city.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_stat_salary_by_city(connect()), ensure_ascii=False))

with open("get_stat_salary_by_job.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_stat_salary_by_job(connect()), ensure_ascii=False))

with open("get_stat_age_by_city.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_stat_age_by_city(connect()), ensure_ascii=False))

with open("get_stat_age_by_job.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_stat_age_by_job(connect()), ensure_ascii=False))

with open("get_max_salary_by_min_age.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_max_salary_by_min_age(connect()), ensure_ascii=False))

with open("get_min_salary_by_max_age.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_min_salary_by_max_age(connect()), ensure_ascii=False))

with open("get_50k_salary_by_avg_age.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_50k_salary_by_avg_age(connect()), ensure_ascii=False))

with open("get_salary_by_city_job_age.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_salary_by_city_job_age(connect()), ensure_ascii=False))

with open("get_salary_by_year_for_manager.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_salary_by_year_for_manager(connect()), ensure_ascii=False))


#insert_many(connect())