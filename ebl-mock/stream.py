import os
import pyvista as pv
from threading import Thread

from replay_converter import ReplayConverter
from ecos_converter import EcosConverter
from transform_data import *

DEVICE_IP = "127.0.0.1"

# dab lap
folder = "./ebl-mock/data/got_raw_files/run8/"
files = ["02_dab"]

# measure trainswitch
folder_ts = "./ebl-mock/data/got_raw_files/run5_ts/"
files_ts = [
    ["dab_ew01_dcc019"],
    ["dab_ew05_dcc014"]
]

dirs = os.listdir(os.path.curdir)

if not os.path.exists(os.path.join(folder, files[0])):
    raise ValueError("you're a donkey.")


def replay_gtcommand():
    """Replay raw got files to socket."""
    rp = ReplayConverter(
        ip_server=DEVICE_IP, files=files, folder=folder, raw_flg=True
    )
    rp.read_input()


if __name__ == "__main__":
    Thread(target=replay_gtcommand, daemon=True).start()

    ec = EcosConverter(ip_server=DEVICE_IP)
    ec.read_input()
