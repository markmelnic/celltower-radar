
import sys

from src.ipinfo import IPINFO
from src.mls import MLS


if __name__ == '__main__':
    try:
        mls = MLS()

        ip = IPINFO()

        mcc_dataset = mls.get_mcc(ip.mcc)

        sorted_dataset = mls.sort_data(mcc_dataset, ip.initial_coords)
    except KeyboardInterrupt:
        sys.exit(0)
