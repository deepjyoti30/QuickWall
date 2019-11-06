#!/usr/bin/env python3
"""Uses unsplash API to set wallpapers from the cli."""

import requests
import argparse

from QuickWall.SetPaper import SetPaper
from QuickWall.utility import (is_nitrogen, clear_cache)
from QuickWall.logger import Logger
from QuickWall.setter import WallSetter
from QuickWall.wall import Wall

from QuickWall.blacklist import Blacklist

# Declare the logger
logger = Logger("main")


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="QuickWall - Quickly set\
                                     latest wallpapers from Unsplash\
                                     directly from the commandline.",
                                     epilog="If you find any bugs, feel\
                                     free to raise an issue in the GitHub\
                                     [https://github.com/deepjyoti30/QuickWall] page.")
    parser.add_argument('--version', action='version', version='0.0.1-4',
                        help='show the program version number and exit')
    parser.add_argument('--clear-cache', help="Clear the cache from the\
                        cache folder (~/.QuickWall)", action='store_true')
    parser.add_argument('--setter', help="Wallpaper setter to be used.\
                        Currently supported ones: nitrogen, feh  (default: nitrogen)",
                        type=str, default="nitrogen")
    parser.add_argument('-d', '--disable-blacklist', help="Disable adding the\
                        image to blacklisted ones.", action="store_true")
    parser.add_argument('--remove-id', help="Remove the passed ID\
                        from the blacklist.", default=None, type=str, metavar="ID")
    parser.add_argument('--dir', help="Directory to download the wallpapers",
                        type=str, default=None)
    parser.add_argument('--id', help="Get a photo by its ID.",
                        type=str, default=None, metavar="ID")
    parser.add_argument('--random', help="Get random wallpapers.",
                        action="store_true")
    parser.add_argument('--search', help="Show wallpapers based on the\
                        passed term", type=str, metavar="TERM")
    args = parser.parse_args()

    return args


def main():
    # Parse the arguments
    args = parse()

    if args.clear_cache:
        clear_cache()
        exit(0)

    if args.remove_id:
        blacklist = Blacklist(args.remove_id).remove_blacklist()
        exit(0)
    
    wall = Wall(photo_id=args.id, random=args.random, search=args.search)

    # Get the wallpaper setter
    wall_setter = WallSetter(args.setter)
    setter = wall_setter.get_setter()

    logger.info("Getting the wallpapers using Unsplash API...")
    paper_list = wall.get_list()

    # If the dir is None, update it
    if args.dir is None:
        args.dir = "~/.QuickWall"

    set_paper = SetPaper(paper_list, setter, args.dir, args.disable_blacklist)
    set_paper.do()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt passed. Exiting..!")
