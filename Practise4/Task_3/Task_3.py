import json
import sqlite3
import msgpack

def read_files(msg_file, text_file):
    items = []
    with open(text_file, "r", encoding='utf-8') as f:
        lines = f.readlines()
    item = dict()
    for line in lines:
        if line == "=====\n":
            items.append(item)
            item = dict()
        else:
            line = line.strip()
            split = line.split("::")

            if split[0] in ["duration_ms", "year"]:
                item[split[0]] = int(split[1])
            elif split[0] in ["tempo", "instrumentalness"]:
                item[split[0]] = float(split[1])
            elif split[0] in ["explicit", "loudness"]:
                continue
            else:
                item[split[0]] = split[1]

    with open(msg_file, 'rb') as file:
        data = msgpack.load(file, raw=False)
        for i in data:
           i["duration_ms"] = int(i["duration_ms"])
           i["year"] = int(i["year"])
           i["tempo"] = float(i["tempo"])
           i["instrumentalness"] = float(i["instrumentalness"])
           del i["speechiness"]
           del i["acousticness"]
           del i["mode"]
           items.append(i)
    #print(items)
    return items


def connect(file_name):
    connection = sqlite3.connect(file_name)
    connection.row_factory = sqlite3.Row
    return connection

def insert_data(db, data):
    cursor = db.cursor()
    cursor.executemany("""
                    INSERT INTO music 
                    (
                        artist,
                        song,
                        duration_ms,
                        year,
                        tempo,
                        genre,
                        instrumentalness
                    )
                    VALUES
                    (:artist, :song, :duration_ms, :year, :tempo, :genre, :instrumentalness)
    """, data)
    db.commit()


def get_top_by_duration_ms(db, limit=38):
    cursor = db.cursor()
    res = cursor.execute("""
                    SELECT * FROM music ORDER BY duration_ms DESC LIMIT ?
    """, [limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    cursor.close()
    #print(items)
    return items


def get_stat_by_year(db):
    cursor = db.cursor()
    res = cursor.execute("""
                        SELECT
                            SUM(year) as sum,
                            AVG(year) as avg,
                            MIN(year) as min,
                            MAX(year) as max
                          from music
                          """)
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    return items

def get_freq_by_artist(db, artist):
    cursor = db.cursor()
    res = cursor.execute("""
        SELECT *
        FROM music
        WHERE artist = ?
         """, [artist])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
    return items

def filter_by_genre(db, genre, limit=43):
    cursor = db.cursor()
    res = cursor.execute("""
                        SELECT *
                        FROM music
                        WHERE genre = ?
                        ORDER BY year
                        LIMIT ?
                          """, [genre, limit])
    items = []
    for row in res.fetchall():
        item = dict(row)
        items.append(item)
        #print(dict(row))
    cursor.close()
    return items



# data = read_files("task_3_var_28_part_2.msgpack", "task_3_var_28_part_1.text")
db = connect("second.db")
# insert_data(db, data)

with open("get_top_by_duration_ms.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_top_by_duration_ms(db, 38), ensure_ascii=False))

with open("get_stat_by_year.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_stat_by_year(db), ensure_ascii=False))

with open("get_freq_by_artist.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(get_freq_by_artist(db, 'LMFAO'), ensure_ascii=False))

with open("filter_by_genre.json", 'w',  encoding="utf-8") as f:
    f.write(json.dumps(filter_by_genre(db,"pop", limit=43), ensure_ascii=False))