import csv
import json
import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes'
table_selector_css = "table.sortable"

page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

# Find all tables and select the first one (Table 0)
all_tables = soup.find_all('table', { "class": "sortable"})
table = all_tables[0]

# Get header indices for required columns
headers = [th.get_text(strip=True) for th in table.find_all('th')]
country_idx = headers.index('ISO 3166[1]name[5]')
iso2_idx = headers.index('A-2[5]')
iso3_idx = headers.index('A-3[5]')
numeric_idx = headers.index('Num.[5]')

country_data = []

# The columns are:
# 0: Country name
# 1: Official state name
# 2: Sovereignty
# 3: ISO2
# 4: ISO3
# 5: Numeric
# 6: ISO 3166-2 link
# 7: TLD

for row in table.find_all('tr')[1:]:
    cells = row.find_all('td')
    if len(cells) < 6:
        continue

    # remove <sup> tags from country name
    for cell in cells:
        for sup in cell.find_all('sup'):
            sup.decompose()

    country = cells[0].get_text(strip=True)
    state_name = cells[1].get_text(strip=True)
    iso2 = cells[3].get_text(strip=True)
    iso3 = cells[4].get_text(strip=True)
    iso3166_2_link = cells[6].get_text(strip=True) #cells[6].find('a')['href'] if cells[6].find('a') else ''
    numeric = cells[5].get_text(strip=True)
    country_data.append({
        'country': country,
        'state_name': state_name,
        'iso2': iso2,
        'iso3': iso3,
        'numeric': numeric,
        'iso3166_2_link': iso3166_2_link
    })

with open('iso_country_codes.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['country', 'state_name', 'iso2', 'iso3', 'numeric', 'iso3166_2_link'])
    writer.writeheader()
    writer.writerows(country_data)

with open('iso_country_codes.json', 'w', encoding="utf-8") as jsonfile:
    json.dump(country_data, jsonfile, indent=2)

# make it column oriented
columns = { 'country': [], 'state_name': [], 'iso2': [], 'iso3': [], 'numeric': [], 'iso3166_2_link': [] }
for item in country_data:
    for key in columns.keys():
        columns[key].append(item[key])
with open('iso_country_codes_columns.json', 'w', encoding="utf-8") as jsonfile:
    json.dump(columns, jsonfile, indent=2)

