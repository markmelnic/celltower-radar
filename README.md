# A set of tools to get all Cell Tower information to use with the Google Geolocation API

![Cellmapper Example](https://i.imgur.com/o9FzO9t.png)

First things first, why did I make this?
The answer is simple and it's the lack of documentation on how to use the Geolocation API in python and actually get it to work.
In theory all the information required can be found in the official [documentation](https://developers.google.com/maps/documentation),
another problem comes up however, where do you find all the data necessary for instance for the Cell Tower Object.
I will thoroughly describe how to use the tools within repository (comments aside), and what is the purpose of each file here.

## [The Mozilla Location Service](https://location.services.mozilla.com) (will be referred to as MLS)

> MLS is an open service, which lets devices determine their location based on network infrastructure like Bluetooth beacons, cell towers and WiFi access points.
This network based location service complements satellite based navigation systems like A-GPS.

MLS offers us a huge dataset containing data for around 50 million unique cells which we can use, in combination with MCC and providers data (will discuss below),
to make proper requests to the API and receive an accurate response. The __mls_handler__ will make the request, download, save, reformat and process the file,
so you shouldn't worry about that.

## [Mobile Country Codes (MCC) and Mobile Network Codes (MNC)](https://www.mcc-mnc.com) (will be referred to as MCCS)

> Mobile Country Codes (MCC) are used in wireless telephone networks (GSM, CDMA, UMTS, etc.) in order to identify the country which a mobile subscriber belongs to.

MCCS is offering a extensive dataset containing all providers, mcc and mnc for every country in the world.
Here it is needed to know how each MCC and country correspond to each other and further identify the MNC, etc.

## [Cellmapper providers list](https://www.cellmapper.net)

Cellmapper is a very nice and interactive tool to visualize and get data for cell towers around you, but it is lacking on data like LAC and cell coordinates.
However, it has a good and clean selector list of providers in each country which will be useful in a later version of this repository, so there's that.
