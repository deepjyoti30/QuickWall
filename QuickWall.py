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
    parser.add_argument('--version', action='version', version='0.0.1-3',
                        help='show the program version number and exit')
    parser.add_argument('--clear-cache', help="Clear the cache from the\
                        cache folder (~/.QuickWall)", action='store_true')
    parser.add_argument('--setter', help="Wallpaper setter to be used.\
                        Currently supported ones: nitrogen, feh  (default: nitrogen)",
                        type=str, default="nitrogen")
    parser.add_argument('--dir', help="Directory to download the wallpapers",
                        type=str, default=None)
    parser.add_argument('--random', help="Get random wallpapers.",
                        action="store_true")
    parser.add_argument('--search', help="Show wallpapers based on the\
                        passed term", type=str, metavar="TERM")
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
    def __init__(self, random=None, search=None):
        self.s_term = None
        self._acces_key = "15bcea145de0b041ec8d3b16bf805e232c83cf52d569a06708aa51f33a4f14f4"
        self._base_URL = "https://api.unsplash.com/photos/"
        self._URL = 'https://api.unsplash.com/photos/?client_id={}&per_page=30'.format(self._acces_key)
        self._URL_list = []
        self.random = random
        self.search = search
        self._build_URL()

    def search(self, name):
        # Update the URL
        self.s_term = name
        logger.info("Searching for {}".format(name))
        self._URL = 'https://api.unsplash.com/search/photos/?query={}&client_id={}&per_page=30'.format(name, self._acces_key)

    def _build_URL(self):
        """Build the URL based on the passed args."""

        self._URL = self._base_URL
        self.params = {
                    'client_id': self._acces_key,
                    'per_page' : 30, 
                }

        if self.random:
            logger.info("Adding random to URL")
            self._URL += "random/"
            self.params['count'] = self.params.pop('per_page')
        if self.search:
            logger.info("Adding search term [{}] to URL".format(self.search))
            self.params.update({'query': self.search})

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
        response = requests.get(self._URL, params=self.params)
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
    
    wall = Wall(random=args.random, search=args.search)

    # Get the wallpaper setter
    wall_setter = WallSetter(args.setter)
    setter = wall_setter.get_setter()

    logger.info("Getting the wallpapers using Unsplash API...")
    paper_list = wall.get_list()

    # If the dir is None, update it
    if args.dir is None:
        args.dir = "~/.QuickWall"

    set_paper = SetPaper(paper_list, setter, args.dir)
    set_paper.do()


if __name__ == '__main__':
    main()
