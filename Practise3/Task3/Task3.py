from bs4 import BeautifulSoup
import numpy as np
import re
import json

def get_num(selector: str, items: list):
    nums = list(map(lambda x: int(x[selector]), items))

    stat = {}

    stat['sum'] = sum(nums)
    stat['min'] = min(nums)
    stat['max'] = max(nums)
    stat['avg'] = np.average(nums)
    stat['std'] = np.std(nums)

    return stat


def get_freq(selector: str, items: list):
    freq = {}

    for item in items:
        if selector in item:
            freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq


def handle_file(file_name):
    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        star = BeautifulSoup(text, 'xml').star

        item = dict()
        for gg in star.contents:
            if gg.name is not None:
                item[gg.name] = gg.get_text().strip()

        return item


items = []
for i in range(1, 501):
    file_name = f"zip_var_28_task3/{i}.xml"
    items.append(handle_file(file_name))
with open("result_3.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items, ensure_ascii=False))
items = sorted(items, key=lambda x: int(x['radius']), reverse=True)

with open("result_sort_radius.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items, ensure_ascii=False))

filtered = []
for item in items:
    if float(item['distance'].replace(' million km', '').strip()) >= 6000000:
        filtered.append(item)

with open("result_filtered_distance.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(filtered, ensure_ascii=False))

#num_stat = get_num("radius", items)
with open("result_num_stat_task3.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(get_num("radius", items), ensure_ascii=False))
#print(num_stat)

#title_freq = get_freq("name", items)
with open("result_get_freq_task3.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(get_freq("name", items), ensure_ascii=False))

#print(title_freq)