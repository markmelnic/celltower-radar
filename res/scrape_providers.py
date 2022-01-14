
import os, json, requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

URL = 'https://www.cellmapper.net/'

def scrape_providers():

    # open file containing html source code
    with open('source.html', 'r', encoding='utf-8') as markup_file:
        markup = markup_file.read()

    soup = BeautifulSoup(markup, "html.parser")
    data = {}

    with open('providers.json', 'w') as json_file:
        for option_group in soup.find(id = 'MNCSelect'):
            try:
                if option_group['label'] == '':
                    continue
                else:
                    data[option_group['label']] = []
                    for option in option_group:
                        provider = {}
                        provider['v'] = option['value']
                        pname = option.get_text().lower().split(' - ')
                        pname = ''.join(pname[:-1])
                        provider['n'] = pname
                        data[option_group['label']].append(provider)
            except KeyError:
                continue

        json.dump(data, json_file)

if __name__ == '__main__':

    scrape_providers()
