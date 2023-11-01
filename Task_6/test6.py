from bs4 import BeautifulSoup
import json

str_json = ''

with open('text_6_var_5', encoding='utf-8') as file:
    lines = file.readlines()
    for line in lines:
        str_json += line

data = json.loads(str_json)
data = data['items']

soup = BeautifulSoup("""<table>
    <tr>
        <th>project</th>
        <th>article</th>
        <th>granularity</th>
        <th>timestamp</th>
        <th>access</th>
        <th>agent</th>
    </tr>
 </table>""", "html.parser")

table = soup.contents[0]
for tick in data:
    tr = soup.new_tag("tr")
    for key, value in tick.items():
        td = soup.new_tag("td")
        td.string = value
        tr.append(td)
    table.append(tr)

with open('r_text_6_var_5.html', 'w') as result:
    result.write(soup.prettify())
    result.write('\n')
