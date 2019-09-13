#!/usr/bin/env python3
"""Uses unsplash API to set wallpapers from the cli."""

import requests
import argparse

from QuickWall.SetPaper import SetPaper
from QuickWall.utility import (is_nitrogen, clear_cache)
from QuickWall.logger import Logger
from QuickWall.setter import WallSetter
from QuickWall import search
from QuickWall import basic
# Declare the logger
logger = Logger("main")


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="QuickWall - Quickly set\
                                     latest wallpapers from Unsplash\
                                     directly from the commandline.")
    parser.add_argument('--version', action='version', version='0.0.1-3',
                        help='show the program version number and exit')
    parser.add_argument('--clear-cache', help="Clear the cache from the\
                        cache folder (~/.QuickWall)", action='store_true')
    parser.add_argument('--setter', help="Wallpaper setter to be used.\
                        Currently supported ones: nitrogen, feh  (default: nitrogen)",
                        type=str, default="nitrogen")
    parser.add_argument('--dir', help="Directory to download the wallpapers",
                        type=str, default=None)
    parser.add_argument('--search', help="Search",type=str)
    args = parser.parse_args()

    return args




def main():
    # Parse the arguments
    args = parse()

    if args.clear_cache:
        clear_cache()
        exit(0)
    
    # Get the wallpaper setter
    wall_setter = WallSetter(args.setter)
    setter = wall_setter.get_setter()

    if args.search:
        wall=search.Wall()
    else:
        wall=basic.Wall()

    logger.info("Gettting the wallpapers using Unsplash API...")
    paper_list = wall.get_list()

    # If the dir is None, update it
    if args.dir is None:
        args.dir = "~/.QuickWall"

    set_paper = SetPaper(paper_list, setter, args.dir)
    set_paper.do()


if __name__ == '__main__':
    main()
