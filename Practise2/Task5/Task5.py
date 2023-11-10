import csv
import numpy as np
import json
import pickle
import msgpack
import os

def most_common(spisok):
    slova = {}
    for col in spisok:
        if col in slova:
            slova[col] += 1
        else:
            slova[col] = 1
    return [(key, value) for key, value in slova.items() if value == max(slova.values())][0]

def saver(stats):
    with open("Motor_Vehicle_Collisions_-_Crashes.json", "w") as r_json:
        r_json.write(json.dumps(stats))

    with open("Motor_Vehicle_Collisions_-_Crashes.pkl", "wb") as f:
        f.write(pickle.dumps(stats))

    with open('Motor_Vehicle_Collisions_-_Crashes.csv', 'w', encoding="utf-8", newline='') as result:
        writer = csv.writer(result, delimiter=',', quotechar='*', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(stats.keys())
        writer.writerow(stats.values())

    with open("Motor_Vehicle_Collisions_-_Crashes.msgpack", "wb") as r_msgpack:
        r_msgpack.write(msgpack.dumps(stats))
    print("Size:")
    print(f"csv        = {os.path.getsize('Motor_Vehicle_Collisions_-_Crashes.csv')}")
    print(f"json       = {os.path.getsize('Motor_Vehicle_Collisions_-_Crashes.json')}")
    print(f"msgpack    = {os.path.getsize('Motor_Vehicle_Collisions_-_Crashes.msgpack')}")
    print(f"pickle     = {os.path.getsize('Motor_Vehicle_Collisions_-_Crashes.pkl')}")


crashes_stat = {}

p_injured = []
p_injured_n = []

p_killed = []

zip_code = []

crash_date = []

with open("Motor_Vehicle_Collisions_-_Crashes.csv", encoding='utf-8') as r_file:
    file_reader = list(csv.reader(r_file, delimiter = ","))
    lines_amount = 100
    first_100 = file_reader[1:lines_amount+1:]
    headers = file_reader[0]
    for line in first_100:
        p_injured.append(line[10])
        p_killed.append(line[11])
        zip_code.append(line[3])
        crash_date.append(line[6])

    for rec in p_injured:
        try:
            if len(rec) <= 3 and rec.isdigit():
                p_injured_n.append(int(rec))
        except:
            print("e")

    crashes_stat["Max people injured"] = max(p_injured)
    crashes_stat["Min people injured"] = min(p_injured)

    #print(p_injured_n)

    crashes_stat["Average injured people"] = sum(p_injured_n)/len(p_injured_n)
    crashes_stat["Standard deviation of injured"] = np.std(p_injured_n)

    crashes_stat["Most common crash date"] = most_common(crash_date)[0]
    crashes_stat["Most common crash date,%"] = most_common(crash_date)[1]/lines_amount * 100

    crashes_stat["Most common injured"] = most_common(p_injured)[0]
    crashes_stat["Most common injured,%"] = most_common(p_injured)[1] / lines_amount * 100

    crashes_stat["Most common zip code"] = most_common(zip_code)[0]
    crashes_stat["Most common zip code,%"] = most_common(zip_code)[1] / lines_amount * 100

    crashes_stat["Most killed"] = most_common(p_killed)[0]
    crashes_stat["Most killed,%"] = most_common(p_killed)[1] / lines_amount * 100


    saver(crashes_stat)