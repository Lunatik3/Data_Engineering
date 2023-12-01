from bs4 import BeautifulSoup
import numpy as np
import re
import json


def get_num(selector: str, items: list):
    nums = list(map(lambda x: x[selector], items))

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
    items = list()

    with open(file_name, encoding="utf-8") as file:
        text = ""
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')
        products = site.find_all("div", attrs={'class': 'product-item'})

        for product in products:
            item = dict()
            item['id'] = product.a['data-id']
            item['link'] = product.find_all('a')[1]['href']
            item['img_url'] = product.find_all('img')[0]['src']
            item['title'] = product.find_all('span')[0].get_text().strip()
            item['price'] = int(product.price.get_text().replace("₽", "").replace(" ", "").strip())
            item["bonus"] = int(product.strong.get_text().replace("+ начислим ", "").replace(" бонусов", "").strip())
            props = product.ul.find_all("li")
            for prop in props:
                item[prop['type']] = prop.get_text().strip()

            items.append(item)

        return items


items = []
for i in range(1, 54):
    file_name = f"zip_var_28_tak2/{i}.html"
    items += handle_file(file_name)
with open("result_2.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items, ensure_ascii=False))

items = sorted(items, key=lambda x: x['price'], reverse=True)

with open("result_sort_price.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(items, ensure_ascii=False))

filtered = []
for item in items:
    if item['bonus'] > 1500:
        filtered.append(item)

with open("result_filtered_bonus.json", 'w', encoding="utf-8") as result:
    result.write(json.dumps(filtered, ensure_ascii=False))

# num_stat = get_num("price", items)
with open("result_num_stat_task2.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(get_num("price", items), ensure_ascii=False))
#print(num_stat)

# title_freq = get_freq("ram", items)
with open("result_get_freq_task2.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(get_freq("ram", items), ensure_ascii=False))
#print(title_freq)