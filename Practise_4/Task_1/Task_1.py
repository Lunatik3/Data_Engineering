import sqlite3
import json

variant = 28

def parser_data(file_name):
        items = []
        with open(file_name, "r", encoding='utf-8') as f:
            lines = f.readlines()
        item = dict()
        for line in lines:
            if line == "=====\n":
                items.append(item)
                item = dict()
            else:
                line = line.strip()
                split = line.split("::")

                if split[0] in ["tours_count", "min_rating", "time_on_game"]:
                    item[split[0]] = int(split[1])
                elif split[0] == "begin":
                    item[split[0]] = float(split[1])
                elif split[0] == "id":
                    continue
                else:
                    item[split[0]] = split[1]

        return items

def connect(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert(db,data):
    cursor = db.cursor()
    cursor.executemany("""
        INSERT INTO chess_tour (name, city, begin, system, tours_count, min_rating, time_on_game) 
        VALUES(
            :name , :city, :begin,
            :system, :tours_count, :min_rating, :time_on_game)""", data)

    db.commit()


# insert(db, items)


def min_rating_top(db, limit):
    cursor = db.cursor()
    res = cursor.execute("SELECT * FROM chess_tour ORDER BY min_rating DESC LIMIT ?", [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        #print(item)
    cursor.close()
    return items

def stat_from_time(db):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(time_on_game) as sum,
            AVG(time_on_game) as avg,
            MIN(time_on_game) as min, 
            MAX(time_on_game) as max
        FROM chess_tour
                        """)
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        #print(dict(res.fetchone()))
    cursor.close()
    return items

def system_freq(db):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            CAST(COUNT(*) as REAL) / (SELECT COUNT(*) FROM chess_tour) as count,
            system
        FROM chess_tour
        GROUP BY system
                        """)
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        #print(dict(row))
    return items


def filter_rating(db, min_rating, limit):
    items = []
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM chess_tour
        WHERE min_rating >= ?
        ORDER BY time_on_game DESC
        LIMIT ?
        """, [min_rating, limit])
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        #print(dict(row))
    cursor.close()
    return items


# items = parser_data('task_1_var_28_item.text')
db = connect('first.db')



# result = db.cursor().execute("SELECT * FROM chess_tour")
# print(result.fetchall())
with open("chess_tour_rating_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(min_rating_top(db, variant + 10), ensure_ascii=False))

with open("chess_tour_time_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(stat_from_time(db), ensure_ascii=False))

with open("chess_tour_system_freq_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(system_freq(db), ensure_ascii=False))

with open("chess_tour_filter_rating_1.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(filter_rating(db, min_rating=2500, limit=38), ensure_ascii=False))

#system_freq(db)
#stat_from_time(db)
#filter_rating(db, min_rating = 2500)