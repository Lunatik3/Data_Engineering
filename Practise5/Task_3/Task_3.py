import pickle
import json
from pymongo import MongoClient

# считываем первый файл
def read_file(filename):
    with open(filename, 'rb') as file:
        data = pickle.load(file)
    return data


def insert_many(collection, data):
    collection.insert_many(data)


def connect():
    client = MongoClient()
    db = client["database_1"]
    return db.person


def delete_salary(collection):
    res = collection.delete_many({"$or":[
                {"salary": {"$lt": 25000}},
                {"salary": {'$gt': 175000}}
    ]})
    print(res)

def update_age(collection):
    res = collection.update_many({}, {"$inc": {"age": 1}})
    print(res)

def up_salary_by_job(collection):
    res = collection.update_many({
        "job": {"$in": ["Программист", "Строитель", "Врач"]}}, {
        "$mul": {"salary": 1.05}})
    print(res)

def up_salary_by_city(collection):
    res = collection.update_many({
        "city": {"$in": ["Севилья", "Хихон", "Виго"]}}, {
        "$mul": {"salary": 1.07}})
    print(res)

def up_salary_city_job(collection):
    res = collection.update_many({
        "$and": [{"city": {"$in": ["Минск", "Аликанте", "Рига"]}},
                {"job": {"$in": ["Инженер", "Медсестра", "Водитель"]}},
                {"age": {"$gt": 38}}]}, {
        "$mul": {"salary": 1.1}})
    print(res)

def delete_by_city_and_salary(collection):
    res = collection.delete_many({
        "$and": [
            {"city": {"$in": ["Будапешт"]}},
            {"salary": {"$gt": 100000}},
        ]
    })
    print(res)


#data = read_file("task_3_item.pkl")
#insert_many(connect(), data)

delete_salary(connect())
update_age(connect())
up_salary_by_job(connect())
up_salary_by_city(connect())
up_salary_city_job(connect())
delete_by_city_and_salary(connect())
