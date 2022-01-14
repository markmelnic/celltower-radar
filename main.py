
import sys

from res.ipinfo import IPINFO
from res.mls_handler import MLS


if __name__ == '__main__':
    try:
        print("Running MLS checks")
        mls = MLS()
        print("Getting IP information")
        ip = IPINFO()
        mcc_dataset = mls.get_mcc(ip.mcc)
        print("Sorting dataset")
        sorted_dataset = mls.sort_data(mcc_dataset, ip.initial_coords)
    except KeyboardInterrupt:
        sys.exit(0)
