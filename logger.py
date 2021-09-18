import time
import getpass
import logging


date = time.strftime("%Y_%m_%d_%H")
user = getpass.getuser()
formatter = logging.Formatter(f"[%(asctime)s] %(levelname)s - {user} - %(message)s",datefmt="%m-%d %H:%M:%S")

logger = logging.getLogger("p2p-leading")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler(f"log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
