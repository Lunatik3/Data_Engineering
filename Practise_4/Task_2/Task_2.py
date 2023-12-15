import sqlite3
import csv
import json

def load_data(file_name):
    items = []

    with open(file_name, "r", encoding='utf-8') as input:
        reader = csv.reader(input, delimiter=";")
        reader.__next__()

        for row in reader:
            if len(row) == 0: continue
            item = dict()
            item['name'] = row[0]
            item['place'] = int(row[1])
            item['prise'] = int(row[2])
            print(item)
            items.append(item)
    return items

def connect(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection




def insert_subitem(db,data):
    cursor = db.cursor()

    cursor.executemany("""
        INSERT INTO subitem (chess_tour_id, place, prise) 
        VALUES(
            (SELECT id from chess_tour WHERE name = :name),
            :place, :prise)""", data)

    db.commit()

def name_2(db, name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT * 
        FROM subitem
        WHERE chess_tour_id = (SELECT id FROM chess_tour WHERE name = ?)                
         """, [name])
    items = []
    for row in res.fetchall():
        item = dict(row)
        print(item)
        items.append(item)
    cursor.close()
    return items


def name_stat_2(db, name):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT 
            SUM(prise) as sum_prise,
            AVG(prise) as avg_prise,
            MIN(prise) as min_prise, 
            MAX(prise) as max_prise
        FROM subitem
        WHERE chess_tour_id = (SELECT id FROM chess_tour WHERE name = ?)  

         """, [name])
    items = []
    for row in res.fetchall():
        item = dict(row)
        print(item)
        items.append(item)
    cursor.close()
    return items

def place_2(db):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT
            begin,
            (SELECT COUNT(*) FROM subitem WHERE id = chess_tour_id) as place
        FROM chess_tour
        ORDER BY place DESC
        LIMIT 38             
         """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        print(item)
        items.append(item)
    cursor.close()
    return items


db = connect('first.db')
#name_2(db, "Алушта 1983")
#name_stat_2(db, "Алушта 1983")
#place_2(db)

with open("name_2.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(name_2(db, 'Алушта 1983'), ensure_ascii=False))

with open("name_stat_2.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(name_stat_2(db, 'Алушта 1983'), ensure_ascii=False))

with open("place_2.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(place_2(db), ensure_ascii=False))

#items = load_data('task_2_var_28_subitem.csv')
#insert_subitem(db,items)