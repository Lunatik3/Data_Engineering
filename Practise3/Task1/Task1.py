from bs4 import BeautifulSoup
import re
import json
import numpy as np

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
        freq[item[selector]] = freq.get(item[selector], 0) + 1

    return freq
def handle_file(file_name):
    with open(file_name, encoding='utf-8') as file:
        text = ''
        for row in file.readlines():
            text += row

        site = BeautifulSoup(text, 'html.parser')

        item = dict()

        genre_raw = site.html.body.div.div.span.get_text()
        item['genre'] = genre_raw.strip().split(':')[1].strip()
        #print(item['genre'])
        item['book-title'] = site.find_all('h1')[0].get_text().strip()
        #print(item['book-title'])
        item['author'] = site.find_all('p')[0].get_text().strip()
        item['pages'] = site.find_all('span', attrs={'class': 'pages'})[0].get_text().split(':')[1].strip().split(' ')[0]
        item['year'] = site.find_all('span', attrs={'class': 'year'})[0].get_text().split('в')[1].strip().split(' ')[0]
        item['isbn'] = site.find_all('span', string=re.compile('ISBN'))[0].get_text().split(':')[1].strip()
        item["description"] = site.find_all("p")[1].get_text().replace("Описание\n", "").strip()
        item["img_url"] = site.find_all("img")[0]['src']
        item["rating"] = site.find_all("span", string=re.compile('Рейтинг:'))[0].get_text().split(':')[1].strip()
        item["views"] = int(site.find_all("span", string=re.compile('Просмотры:'))[0].get_text().split(':')[1].strip())

        return item


items = []
for i in range(1, 1000):
    file_name = f"zip_var_28/{i}.html"
    items.append(handle_file(file_name))
#json_items = json.dumps(items)
with open("result.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(items, ensure_ascii=False))

views = []
for i in range(1, 1000):
    file_name = f"zip_var_28/{i}.html"
    views.append(handle_file(file_name))
views = sorted(views, key=lambda x: x['views'], reverse=True)
#json_views = json.dumps(views)
with open("result_views.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(views, ensure_ascii=False))


genre = []
for book in items:
    if book['genre'] == "научная фантастика":
        genre.append(book)
with open("result_genre.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(genre, ensure_ascii=False))
#print(len(genre))
#print(len(items))

#num_stat = get_num("views", items)
with open("result_num_stat_task1.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(get_num("views", items), ensure_ascii=False))
#print(num_stat)

# city_freq = get_freq("author", items)
with open("result_get_freq_task1.json", "w", encoding="utf-8") as result:
    result.write(json.dumps(get_freq("author", items), ensure_ascii=False))
#print(city_freq)