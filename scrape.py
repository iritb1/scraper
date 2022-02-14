
from bs4 import BeautifulSoup
import requests
import re


res = requests.get('https://en.m.wikipedia.org/wiki/List_of_animal_names')
soup = BeautifulSoup(res.text, features="html.parser")

data = []
animals = {}

table = soup.find_all('table', attrs = {'class': 'wikitable sortable'})[1] #css selector get element by tag name

table_body = table.find('tbody')
rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) #get rid of empty values

cleared_data = ([x for x in data if x])

#creating dict {animal:collateral adjectives} and removing any strange characters like '?' and more
for arr in cleared_data:
    key = re.sub(r'[^a-zA-Z]', '', arr[0])
    val = re.sub(r'[^a-zA-Z]', '', arr[len(arr)-1])
    animals[key] = val

print(animals)

#creating html file with the animals:
text = '''
<html>
    <header>
        <table border=1 style='text-align:center'>
        <tr>
            <th>animal</th>
            <th>collateral adjectives</th>
        </tr>
'''

table = ""
for animal, collateral_adjective in animals.items():
    table = table + f"""<tr>
        <td>{animal}</td>
        <td>{collateral_adjective}</td>
    </tr>     
    """

text = text + table + '</table> </header> </html>'

file = open("animals.html","w")
file.write(text)
file.close()




