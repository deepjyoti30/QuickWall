"""All utility related functions defined here"""

import subprocess

from pathlib import Path
from shutil import rmtree
from os import mkdir

from QuickWall.logger import Logger


# Declare logger
logger = Logger("Utility")


def is_nitrogen():
    """
    Check if nitrogen is present or not
    """
    command = "nitrogen --help"
    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    ret, err = p.communicate()

    return True if err is None else False


def is_feh():
    """
    Check if feh is installed.
    """
    command = "feh --help"

    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    ret, err = p.communicate()

    return True if err is None else False


def clear_cache(dir="~/.QuickWall"):
    """
    Clear the cache from the QuickWall dir
    """
    dir_path = Path(dir).expanduser()
    logger.info("Removing {}".format(dir_path))

    if dir_path.exists():
        rmtree(dir_path)
        mkdir(dir_path)
    else:
        logger.warning("{}: Does not exist".format(dir))
