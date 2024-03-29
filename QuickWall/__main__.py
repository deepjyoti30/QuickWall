#!/usr/bin/env python3
"""Uses unsplash API to set wallpapers from the cli."""

import requests
import argparse
from pathlib import Path

from QuickWall.SetPaper import SetPaper
from QuickWall.utility import (
    is_nitrogen,
    clear_cache,
    migrate_to_new_loc
)
from simber import Logger
from QuickWall.setter import WallSetter
from QuickWall.wall import Wall

from QuickWall.blacklist import Blacklist

# Declare the logger
LOGGER_OUTTEMPLATE = "%a[{logger}]%"
LOGGER_FILEFORMAT = "[{logger}] [{levelname}] [{time}] [{lineno}]"
logger = Logger(
    "main",
    log_path=Path('~/.cache/QuickWall/logs/log.cat').expanduser(),
    format=LOGGER_OUTTEMPLATE,
    file_format=LOGGER_FILEFORMAT,
    update_all=True
)


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="QuickWall - Quickly set\
                                     latest wallpapers from Unsplash\
                                     directly from the commandline.",
                                     epilog="If you find any bugs, feel\
                                     free to raise an issue in the GitHub\
                                     [https://github.com/deepjyoti30/QuickWall] page.")
    parser.add_argument('--version', action='version', version='0.0.5',
                        help='show the program version number and exit')
    parser.add_argument('--clear-cache', help="Clear the cache from the\
                        cache folder (~/.cache/QuickWall)", action='store_true')
    parser.add_argument('--setter', help="Wallpaper setter to be used.\
                        Currently supported ones: nitrogen, feh, xfce, kde, gnome, unity\
                          (default: auto)",
                        type=str, default="auto")
    parser.add_argument('-d', '--disable-blacklist', help="Disable adding the\
                        image to blacklisted ones.", action="store_true")
    parser.add_argument('-t', '--disable-theme', help="Disable setting a colorscheme extracted from the wallpaper",
                        action="store_true", default=False)
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
    parser.add_argument('--migrate', help="ONLY FOR EARLY USERS. Move the files\
                        from ~/.QuickWall to ~/.cache/QuickWall.", action="store_true")
    parser.add_argument('--set-lockscreen', help="Set lockscreen wallpaper (currently for KDE)",
                        action='store_true')

    logger_group = parser.add_argument_group("Logger")
    logger_group.add_argument(
        "--level",
        help="The level of the logger that will be used while verbosing.\
            Use `--list-level` to check available options." + "\n",
        default="INFO",
        type=str
    )
    logger_group.add_argument(
        "--list-level",
        help="List all the available logger levels.",
        action="store_true"
    )

    args = parser.parse_args()

    return args


def main():
    # Parse the arguments
    args = parse()

    if args.list_level:
        logger.list_available_levels()
        exit(0)

    # Update the logger flags, in case those are not the default ones.
    if args.level.lower != "info":
        logger.update_level(args.level.upper())

    # Log the args passed
    logger.debug("args passed: ", str(args))

    if args.clear_cache:
        clear_cache()
        exit(0)

    if args.migrate:
        migrate_to_new_loc()
        exit(0)

    if args.remove_id:
        blacklist = Blacklist(args.remove_id).remove_blacklist()
        exit(0)

    wall = Wall(photo_id=args.id, random=args.random, search=args.search)

    # Get the wallpaper setter
    wall_setter = WallSetter(args.setter, args.set_lockscreen)
    setter = wall_setter.get_setter()

    logger.info("Getting the wallpapers using Unsplash API...")
    paper_list = wall.get_list()

    # If the dir is None, update it
    if args.dir is None:
        args.dir = "~/.cache/QuickWall"

    set_paper = SetPaper(paper_list, setter, args.dir,
                         args.disable_blacklist, disable_theme=args.disable_theme)
    set_paper.do()


def main_handler():
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Keyboard Interrupt passed. Exiting..!")


if __name__ == '__main__':
    main_handler()
