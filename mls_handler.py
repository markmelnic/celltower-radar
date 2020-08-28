
import os, csv, json, shutil, requests, gzip
import pandas as pd
from bs4 import BeautifulSoup

from scrape_mccs import scrape_mccs

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

MLS_URL = 'https://location.services.mozilla.com/downloads'
MLS_CSV = 'mls.csv'

# download MLS file
def download():

    # find MLS file link
    page = requests.get(MLS_URL, headers = HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')

    mls_file_link = soup.find_all('ul')[1].find_all('li')[0].find('a')['href']
    file_credentials = soup.find_all('ul')[1].find_all('li')[0].get_text()

    # download MLS file
    print('Downloading MLS file:', file_credentials)
    mls_filename = mls_file_link.split('/')[-1]
    with requests.get(mls_file_link, stream=True) as r:
        print(r.raw)
        with open(mls_filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

    # extract from zip
    with gzip.open(mls_filename, 'rb') as mls_zip_in:
        with open(MLS_CSV, 'wb') as mls_zip_out:
            shutil.copyfileobj(mls_zip_in, mls_zip_out)

    os.remove(mls_filename)
    reformat_mls()

# remove useless MLS file columns
def reformat_mls():
    dataset = read_mls()
    del dataset['range'], dataset['samples'], dataset['changeable'], dataset['created'], dataset['updated'], dataset['averageSignal'], dataset['unit']
    dataset.to_csv(MLS_CSV, encoding='utf-8', index=False)

# integrate cells to mmcs file
def integrate_cells():
    try:
        with open('mccs.json') as json_file:
            mcc_data = json.load(json_file)
    except FileNotFoundError:
        scrape_mccs()
        with open('mccs.json') as json_file:
            mcc_data = json.load(json_file)

    with open(MLS_CSV, mode="r", newline='') as csv_file:
        csv_reader = csv.reader(csv_file)
        csv_data = list(csv_reader)
        csv_data.pop(0)

    for i, row in enumerate(csv_data):
        for country in mcc_data:
            if int(row[1]) == mcc_data[country]['mcc']:
                for mnc in mcc_data[country]['networks']:
                    if int(row[2]) == mnc['mnc']:
                        if row[0] not in mnc:
                            mcc_data[country]['networks'][mcc_data[country]['networks'].index(mnc)][row[0]] = []
                        ds = {}
                        ds['LAC'] = row[3]
                        ds['cellId'] = row[4]
                        ds['lng'] = row[5]
                        ds['lat'] = row[6]
                        mcc_data[country]['networks'][mcc_data[country]['networks'].index(mnc)][row[0]].append(ds)

    with open('mccs.json', 'w') as json_file:
        json.dump(mcc_data, json_file)

# read MLS file and return pd dataframe
def read_mls() -> list:
    try:
        dataset = pd.read_csv(MLS_CSV)
    except FileNotFoundError:
        download()
        dataset = pd.read_csv(MLS_CSV)
    return dataset

# get all data for specific MCC
def get_mcc(csv_data : list, mcc : int) -> list:
    return csv_data[csv_data["mcc"] == mcc]

if __name__ == '__main__':

    #print(read_mls())
    integrate_cells()
