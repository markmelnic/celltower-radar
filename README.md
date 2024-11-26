# Warning! Mozilla Location Service has been discontinued. This project is no longer maintained.

This project relied on the Mozilla Location Service (MLS) to provide cell tower data. However, MLS has been discontinued, and the service is no longer available.

[https://discourse.mozilla.org/t/retiring-the-mozilla-location-service/128693](https://discourse.mozilla.org/t/retiring-the-mozilla-location-service/128693)

---

# Cell Tower data tools for Google Geolocation API

![Cellmapper Example](https://i.imgur.com/o9FzO9t.png)

## Overview

This repository provides a comprehensive set of tools for retrieving and processing cell tower data for use with the Google Geolocation API. It addresses the lack of detailed documentation and simplifies the process of collecting and using necessary information, such as Cell Tower Object data.

## Data Sources

### [Mozilla Location Service (MLS)](https://location.services.mozilla.com)

> MLS is an open service that allows devices to determine their location based on network infrastructure such as Bluetooth beacons, cell towers, and Wi-Fi access points. This network-based location service complements satellite-based systems like A-GPS.

MLS provides a large dataset of around 50 million unique cell towers. This dataset, combined with MCC and provider data, enables accurate API requests. The `mls` module manages the request, download, reformatting, and processing of the data.

### [Mobile Country Codes (MCC) and Mobile Network Codes (MNC)](https://www.mcc-mnc.com)

> MCC and MNC are used in wireless networks (GSM, CDMA, UMTS, etc.) to identify the country and network provider associated with a mobile subscriber.

This dataset is essential for linking MCC codes to countries and their respective network providers.

### [CellMapper Providers List](https://www.cellmapper.net)

CellMapper is a useful tool for visualizing and collecting data on nearby cell towers. While it lacks some details like Location Area Code (LAC) and exact coordinates, its provider list by country can be useful for future enhancements.

## Features

### Main Functionality

`main.py` orchestrates the entire process of generating the dataset and sorting cell towers based on proximity to your location. It outputs the closest towers to your IP-based location.

To run:
```bash
python main.py
```

*Note: Processing the dataset (around 50 million records) may take some time.*

### Available Resources

- **`mls.py`**: Processes MLS data.
- **`scrape_mccs.py`**: Scrapes MCC codes to enhance the MLS dataset.
- **`scrape_providers.py`**: Scrapes provider details from CellMapper (not currently utilized).
- **`utils.py`**: Contains additional utilities (not currently utilized).
- **`ipinfo.py`**: Retrieves location based on your IP address and identifies the corresponding MCC.

## Usage Example

Below is a usage example demonstrating how to generate a sorted list of cell towers:

```python
from iploc.loc_tools import ipinfo
from src.mls import MLS

if __name__ == '__main__':
    mls = MLS()

    ip = ipinfo()

    mcc_dataset = mls.get_mcc(ip.mcc)

    sorted_dataset = mls.sort_data(mcc_dataset, ip.initial_coords)
```

- `ip.initial_coords` retrieves your coordinates based on your IP address. For higher accuracy, you can supply your own coordinates.
- `sorted_dataset` contains cell towers sorted by proximity. `sorted_dataset[0]` is the closest tower.

## Contribution

Contributions are welcome! Feel free to submit a pull request or open an issue for suggestions, feature requests, or bug reports.

## License

This project is licensed under the MIT License. See `LICENSE` for more details.
