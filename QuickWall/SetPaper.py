"""Functions related to setting the wallpaper."""

from pathlib import Path
from os import makedirs, remove

from QuickWall.download import download
from QuickWall.logger import Logger
from QuickWall.blacklist import Blacklist


# Declare the logger
logger = Logger("SetPaper")


class SetPaper:
    """
    Download the wallpaper and set it using nitrogen.
    """
    def __init__(self, entity_list, setter):
        self.entity_list = entity_list
        self._dir_path = Path('~/.QuickWall').expanduser()
        makedirs(self._dir_path, exist_ok=True)
        self.setter_type = setter  # Update by calling the following function

    def _dw(self, url):
        """
        Download the file using a download manager.
        """
        download(url, self._file_path)

    def _restore(self):
        """
        Restore the wallpaper.
        """
        self.setter_type.restore()

    def _set(self):
        """
        Set the wallpaper.
        """
        self.setter_type.set(self._file_path)

    def _set_perma(self):
        """
        Set the wallpaper permanently
        """
        self.setter_type.set_perm(self._file_path)

    def _is_exists(self):
        """
        Check if the wallpaper already exists.
        """
        return self._file_path.exists()

    def do(self):
        for entity in self.entity_list:
            # Check if blacklisted. If yes, skip to next paper
            blacklist = Blacklist(entity['unique_id'])
            if blacklist.is_blacklisted():
                logger.debug("Found in blacklisted ones")
                continue

            self.desc = entity['desc']
            self.name = entity['name']
            self._file_path = self._dir_path.joinpath('{}.jpg'.format(entity['unique_id']))
            logger.info("{} by {}".format(self.desc, self.name))

            if not self._is_exists():
                self._dw(entity['dw_link'])

            self._set()
            # Interaction
            ask = input("Save this wallpapers? [Y]es [N]o [E]xit ")
            if ask.lower() == 'y':
                self._set_perma()
                exit()
            elif ask.lower() == 'e':
                remove(self._file_path)
                blacklist.add_blacklist()
                self._restore()
                exit()
            else:
                blacklist.add_blacklist()
                self._restore
                remove(self._file_path)
