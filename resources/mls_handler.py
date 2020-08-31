
import os, csv, json, shutil, requests, gzip
import pandas as pd
from bs4 import BeautifulSoup
from scipy import spatial
from geopy.distance import great_circle

from resources.utils import cartesian
from resources.scrape_mccs import scrape_mccs, MCCS_JSON

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

MLS_URL = 'https://location.services.mozilla.com/downloads'
MLS_CSV = './resources/mls.csv'

# execte the entire MLS process
class MLS:
    def __init__(self):

        if not os.path.exists(MLS_CSV):
            print('*MLS file not found, this will take a while')
            print('*(1/5) Downloading MLS zip')

            self.download()
            downloaded = True
            print('*(3/5) Reformatting MLS file')
            self.reformat_mls()
        else:
            downloaded = False
            print('*(1-3/5) Existing MLS file found')

        if not os.path.exists(MCCS_JSON):
            print('*(4/5) Scraping MCCS')
            scrape_mccs()
        else:
            print('*(4/5) Existing MCCS file found')

        if downloaded:
            if hasattr('MLS', 'csv_data') == False:
                self.read_mls()
            print('*(5/5) Integrating MLS and MCCS files')
            #integrate_to_mccs()
            self.integrate_to_csv()
        else:
            print('*(5/5) MLS and MCCS files have been integrated')

        if hasattr('MLS', 'csv_data') == False:
            print('*Reading MLS file')
            self.read_mls()
        print("*Successful MLS handling")

    # download MLS file
    def download(self, ):

        # find MLS file link
        page = requests.get(MLS_URL, headers = HEADERS)
        soup = BeautifulSoup(page.content, 'html.parser')

        mls_file_link = soup.find_all('ul')[1].find_all('li')[0].find('a')['href']
        file_credentials = soup.find_all('ul')[1].find_all('li')[0].get_text()

        # download MLS file
        print('*' + file_credentials.replace('\n', ''))
        mls_filename = mls_file_link.split('/')[-1]
        with requests.get(mls_file_link, stream=True) as r:
            with open(mls_filename, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

        # extract from zip
        print('*(2/5) Extracting MLS file')
        with gzip.open(mls_filename, 'rb') as mls_zip_in:
            with open(MLS_CSV, 'wb') as mls_zip_out:
                shutil.copyfileobj(mls_zip_in, mls_zip_out)

        os.remove(mls_filename)

    # remove useless MLS file columns
    def reformat_mls(self, ):
        self.read_mls()
        with open(MLS_CSV, mode="w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            self.csv_data[0][2] = 'mnc'
            cols_to_remove = sorted([5, 8, 9, 10, 11, 12, 13], reverse=True)
            for row in self.csv_data:
                for index in cols_to_remove:
                    del row[index]
            csv_writer.writerows(self.csv_data)

    # integrate cells to mmcs file
    def integrate_to_mccs(self, ):
        try:
            with open(MCCS_JSON) as json_file:
                mcc_data = json.load(json_file)
        except FileNotFoundError:
            scrape_mccs()
            with open(MCCS_JSON) as json_file:
                mcc_data = json.load(json_file)

        for i, row in enumerate(self.csv_data):
            if i == 0:
                continue
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
                        break
                break

        with open(MCCS_JSON, 'w') as json_file:
            json.dump(mcc_data, json_file)

    # integrate cells to mmcs file
    def integrate_to_csv(self, ):
        try:
            with open(MCCS_JSON) as json_file:
                mcc_data = json.load(json_file)
        except FileNotFoundError:
            self.scrape_mccs()
            with open(MCCS_JSON) as json_file:
                mcc_data = json.load(json_file)

        # define new columns
        self.csv_data[0].append('country')
        self.csv_data[0].append('provider')
        #self.csv_data[0].append('iso')
        #self.csv_data[0].append( 'country code')

        with open(MLS_CSV, mode="w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for i, row in enumerate(self.csv_data):
                if i == 0:
                    continue
                for country in mcc_data:
                    if int(row[1]) == mcc_data[country]['mcc']:
                        self.csv_data[i].append(country)
                        for ntw in mcc_data[country]['networks']:
                            if int(row[2]) == mcc_data[country]['networks'][mcc_data[country]['networks'].index(ntw)]['mnc']:
                                self.csv_data[i].append(mcc_data[country]['networks'][mcc_data[country]['networks'].index(ntw)]['network'])
                                break
                        break
            csv_writer.writerows(self.csv_data)

    # read MLS file and return pd dataframe
    def read_mls(self, ) -> list:
        with open(MLS_CSV, mode="r", newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.csv_data = list(csv_reader)

    # get all data for specific MCC
    def get_mcc(self, mcc : int) -> list:
        return [row for i, row in enumerate(self.csv_data) if i != 0 and int(row[1]) == mcc]

    # find closest 20 towers to ip coordinates
    def sort_data(self, mcc_dataset : list, ic : tuple) -> list:
        '''Return a list of cell towers sorted by proximity to your coordinates.'''
        # mcc_dataset rows
        # row[6] - latitude
        # row[5] - longitude

        coordinates = [(float(row[6]), float(row[5])) for row in mcc_dataset]

        distances = [(i, great_circle(coord, ic)) for i, coord in enumerate(coordinates)]

        sorted_dist = sorted(zip([i[0] for i in distances], [i[1] for i in distances]), key=lambda t: t[1])
        sorted_data = [mcc_dataset[item[0]] for item in sorted_dist]
        return sorted_data

if __name__ == '__main__':

    mls = MLS()
