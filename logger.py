import sys
import getpass
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
user = getpass.getuser()
formatter = logging.Formatter(
    f"[%(asctime)s] %(levelname)s - {user} - %(message)s", datefmt="%m-%d %H:%M:%S"
)


# System output logger (required to see the outputs when executing with Bazel)
sys_handler = logging.StreamHandler(sys.stdout)
sys_handler.setLevel(logging.INFO)
logger.addHandler(sys_handler)

# File logger
file_handler = logging.FileHandler(f"log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
