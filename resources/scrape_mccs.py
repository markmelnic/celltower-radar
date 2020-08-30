
import json, requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

MCCS_URL = 'https://www.mcc-mnc.com/'
MCCS_JSON = './resources/mccs.json'

def scrape_mccs():

    page = requests.get(MCCS_URL, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    data = {}
    with open(MCCS_JSON, 'w') as json_file:
        for row in soup.find('tbody'):
            if row == '\n':
                continue
            row_items = [item.text for item in row]

            if row_items[1] == 'n/a' or row_items[4] == '':
                continue
            if row_items[3] not in data:
                data[str(row_items[3])] = {}
                data[str(row_items[3])]['mcc'] = int(row_items[0])
                data[str(row_items[3])]['iso'] = row_items[2]
                data[str(row_items[3])]['country code'] = int(row_items[4])
                data[str(row_items[3])]['networks'] = []
            line = {}
            line['mnc'] = int(row_items[1])
            line['network'] = row_items[5][:-1]
            data[str(row_items[3])]['networks'].append(line)

        json.dump(data, json_file)

if __name__ == '__main__':

    scrape_mccs()
