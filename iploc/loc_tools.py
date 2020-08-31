
import sys
sys.path.append('../')

import requests, json
from resources.scrape_mccs import MCCS_JSON

HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

IP_URL = 'https://ipinfo.io/json'

class ipinfo:
    def __init__(self):
        self.iso, self.initial_coords = self.get_ip_data()
        self.mcc = self.country_mcc(self.iso)

    # get ip address information to find initial location
    def get_ip_data(self, ):

        response = requests.get(IP_URL, headers = HEADERS)
        data = json.loads(response.text)

        return data['country'].lower(), (data['loc'])

    # get country corresponding MCC
    def country_mcc(self, country : str) -> int:
        with open(MCCS_JSON) as json_file:
            mcc_data = json.load(json_file)

        for item in mcc_data:
            if country == mcc_data[item]['iso']:
                return int(mcc_data[item]['mcc'])

if __name__ == '__main__':

    ipinfo()
