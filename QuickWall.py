#!/usr/bin/env python3
"""Uses unsplash API to set wallpapers from the cli."""

import requests
import argparse

from QuickWall.SetPaper import SetPaper
from QuickWall.utility import (is_nitrogen, clear_cache)
from QuickWall.logger import Logger
from QuickWall.setter import WallSetter


# Declare the logger
logger = Logger("main")


def parse():
    """Parse the arguments."""
    parser = argparse.ArgumentParser(description="QuickWall - Quickly set\
                                     latest wallpapers from Unsplash\
                                     directly from the commandline.")
    parser.add_argument('--version', action='version', version='0.0.1-2',
                        help='show the program version number and exit')
    parser.add_argument('--clear-cache', help="Clear the cache from the\
                        cache folder (~/.QuickWall)", action='store_true')
    parser.add_argument('--setter', help="Wallpaper setter to be used.\
                        Currently supported ones: nitrogen, feh  (default: nitrogen)",
                        type=str, default="nitrogen")

    args = parser.parse_args()

    return args


class Wall:
    """
    Class to do tasks like downloading the wallpaper.

    URL list has 4 entries:

    desc: Description of the image
    name: Name of the user who uploaded the image
    dw_link: Download link of the image
    unique_id: ID to save the image
    """
    def __init__(self):
        self._acces_key = "15bcea145de0b041ec8d3b16bf805e232c83cf52d569a06708aa51f33a4f14f4"
        self._URL = 'https://api.unsplash.com/photos/?client_id={}&per_page=30'.format(self._acces_key)
        self._URL_list = []

    def _add_to_list(self, entity):
        """
        Extract the data from the passed entity and add it to
        the list.
        """

        desc = entity['description']
        if desc is None:
            desc = entity['alt_description']

        if desc is None:
            desc = "Wallpaper"

        name = entity['user']['name']
        dw_link = entity['links']['download']
        unique_id = entity['id']

        self._URL_list.append({
                                'dw_link': dw_link,
                                'unique_id': unique_id,
                                'desc': desc,
                                'name': name
                              })

    def _get_paper(self):
        """
        Get a list of wallpaper using the access key.

        Return a iterable list of direct download URL's.
        """
        response = requests.get(self._URL)
        json_data = response.json()

        for i in json_data:
            self._add_to_list(i)

    def get_list(self):
        self._get_paper()
        return self._URL_list


def main():
    # Parse the arguments
    args = parse()

    if args.clear_cache:
        clear_cache()
        exit(0)

    # Get the wallpaper setter
    wall_setter = WallSetter(args.setter)
    setter = wall_setter.get_setter()

    wall = Wall()
    logger.info("Gettting the wallpapers using Unsplash API...")
    paper_list = wall.get_list()

    set_paper = SetPaper(paper_list, setter)
    set_paper.do()


if __name__ == '__main__':
    main()
