"""All utility related functions defined here"""

import subprocess

from pathlib import Path
from shutil import rmtree, move
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


def clear_cache(dir="~/.cache/QuickWall"):
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


def migrate_to_new_loc():
    """Move the files from the older dir to the new cache location."""
    src = Path("~/.QuickWall").expanduser()
    des = Path("~/.cache/QuickWall").expanduser()

    if not des.exists():
        mkdir(des)

    for file_ in src.iterdir():
        move(str(file_), str(des))
