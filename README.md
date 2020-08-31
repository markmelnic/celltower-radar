# A set of tools to get all Cell Tower information to use with the Google Geolocation API

![Cellmapper Example](https://i.imgur.com/o9FzO9t.png)

## Data sources

First things first, why did I make this?
The answer is simple and it's the lack of documentation on how to use the Geolocation API in python and actually get it to work.
In theory all the information required can be found in the official [documentation](https://developers.google.com/maps/documentation),
another problem comes up however, where do you find all the data necessary for instance for the Cell Tower Object.
I will thoroughly describe how to use the tools within repository (comments aside), and what is the purpose of each file here.

### [The Mozilla Location Service](https://location.services.mozilla.com) (will be referred to as MLS)

> MLS is an open service, which lets devices determine their location based on network infrastructure like Bluetooth beacons, cell towers and WiFi access points.
This network based location service complements satellite based navigation systems like A-GPS.

MLS offers us a huge dataset containing data for around 50 million unique cells which we can use, in combination with MCC and providers data (will discuss below),
to make proper requests to the API and receive an accurate response. The __mls_handler__ will make the request, download, save, reformat and process the file,
so you shouldn't worry about that.

### [Mobile Country Codes (MCC) and Mobile Network Codes (MNC)](https://www.mcc-mnc.com) (will be referred to as MCCS)

> Mobile Country Codes (MCC) are used in wireless telephone networks (GSM, CDMA, UMTS, etc.) in order to identify the country which a mobile subscriber belongs to.

MCCS is offering a extensive dataset containing all providers, mcc and mnc for every country in the world.
Here it is needed to know how each MCC and country correspond to each other and further identify the MNC, etc.

### [Cellmapper providers list](https://www.cellmapper.net)

Cellmapper is a very nice and interactive tool to visualize and get data for cell towers around you, but it is lacking on data like LAC and cell coordinates.
However, it has a good and clean selector list of providers in each country which will be useful in a later version of this repository, so there's that.

## Description of functionality

### Main

`main.py` is intended to run all modules of this repository to generate the dataset and return the list of cell towers closest to your IP based location
in ascending order by proximity in km.

Execute `py main.py` to run the entire process as intended. Take into consideration that the dataset has around 50 million cells recorded,
so computing through them will take a while (on my machine it takes around 15 minutes).

### Resources

  __mls_handler.py__ contains the MLS oject, which is meant to run through all MLS procedures to generate the complete dataset.
  
  __scrape_mccs.py__ will scrape the mcc codes used to complete the MLS dataset.
  
  __scrape_providers.py__ scrapes the providers of each country from cellmapper but is not currently used.
  
  __utils.py__ has some utilities which are not used currently.
  
```
# generate the MLS object
from resources.mls_handler import MLS
mls = MLS()
mls.csv
```

### iploc (stands for IP Location)

__loc_tools.py__ houses the ipinfo object which extracts your location based on ip address and finds the corresponding MCC.

```
# generate the iploc object
from iploc.loc_tools import ipinfo
ip = ipinfo()
```

## Example

This is basically just a copy of `main.py`

```
from iploc.loc_tools import ipinfo
from resources.mls_handler import MLS

if __name__ == '__main__':
    print("Running MLS checks")
    mls = MLS()
    print("Getting IP information")
    ip = ipinfo()
    mcc_dataset = mls.get_mcc(ip.mcc)
    print("Sorting dataset")
    sorted_dataset = mls.sort_data(mcc_dataset, ip.initial_coords)
```

sorted_dataset has each tower sorted by proximity to your location which means, by index:

sorted_dataset[0] is the closest

sorted_dataset[1] is the next and so on

# I hope you'll find this repository useful and don't hesitate to contact me if you have any questions, suggestions, etc. Contributions are warmly welcomed!
