import requests
from bs4 import BeautifulSoup
import json

str_json = ""
with open("test6.json", encoding="utf-8") as file:
    lines = file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
data = data['created']

soup = BeautifulSoup("""<table>
    <tr>
        <th>id</th>
        <th>title</th>
        <th>description</th>
        <th>price</th>
        <th>discountPercentage</th> 
        <th>rating</th>
        <th>stock</th>
        <th>brand</th>
        <th>category</th>           
    </tr>
</table>""", features="html.parser")

table = soup.contents[0]

for tick in data:
    tr = soup.new_tag("tr")
    for key, val in tick.items():
        td = soup.new_tag("td")
        td.string = str(val)
        tr.append(td)
    table.append(tr)

with open("task_6.html", "w", encoding="utf-8") as result:
    result.write(soup.prettify())
    result.write("\n")

