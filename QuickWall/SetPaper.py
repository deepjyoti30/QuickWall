"""Functions related to setting the wallpaper."""

from pathlib import Path
from os import makedirs, remove

from QuickWall.download import download
from QuickWall.logger import Logger
from QuickWall.utility import (is_nitrogen, is_feh)
from QuickWall.nitrogen import nitrogen
from QuickWall.feh import feh


# Declare the logger
logger = Logger("SetPaper")


class SetPaper:
    """
    Download the wallpaper and set it using nitrogen.
    """
    def __init__(self, entity):
        self._url = entity['dw_link']
        self._dir_path = Path('~/.QuickWall').expanduser()
        makedirs(self._dir_path, exist_ok=True)
        self._file_path = self._dir_path.joinpath(entity['unique_id'] + '.jpg')
        self.desc = entity['desc']
        self.name = entity['name']
        self.setter_type = ''  # Update by calling the following function
        self._select_setter()

    def _select_setter(self):
        """
        Select the wallpaper setter to be used.
        """
        if is_nitrogen():
            logger.info("Using nitrogen")
            self.setter_type = nitrogen()
        elif is_feh():
            logger.info("Using feh")
            self.setter_type = feh()
        else:
            logger.critical("No wallpaper setter found. Check the\
                github page for details.")

    def _dw(self):
        """
        Download the file using a download manager.
        """
        download(self._url, self._file_path)

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
        logger.info("{} by {}".format(self.desc, self.name))

        if not self._is_exists():
            self._dw()

        self._set()
        # Interaction
        ask = input("Save this wallpapers? [Y]es [N]o [E]xit ")
        if ask.lower() == 'y':
            self._set_perma()
            exit()
        elif ask.lower() == 'e':
            self._restore()
            exit()
        else:
            self._restore
            remove(self._file_path)
