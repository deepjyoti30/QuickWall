"""Functions related to setting the wallpaper."""

from pathlib import Path
from os import makedirs, remove

from QuickWall.download import download
from QuickWall.logger import Logger
from QuickWall.blacklist import Blacklist
from QuickWall.wal import Wal


# Declare the logger
logger = Logger("SetPaper")


class SetPaper:
    """
    Download the wallpaper and set it using nitrogen.
    """
    def __init__(
                    self,
                    entity_list,
                    setter, passed_dir="~/.cache/QuickWall",
                    disable_blacklist=False,
                    disable_theme=False
                ):
        self.entity_list = entity_list
        self._dir_path = Path(passed_dir).expanduser()
        self._exists()
        makedirs(self._dir_path, exist_ok=True)
        self.setter_type = setter  # Update by calling the following function
        self.disable_blacklist = disable_blacklist
        self._disable_theme = disable_theme

        if not self._disable_theme:
            # Declare a wal object
            self.wal = Wal()
        else:
            logger.info("Skipping setting theme")

    def _exists(self):
        """
        Check if the dir exists, if it doesn't raise an error.
        """
        if not self._dir_path.exists():
            logger.critical("Passed dir does not exist. Quitting!")
        else:
            logger.info("Saving images to {}".format(self._dir_path))

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
        if not self._disable_theme:
            self.wal.restore()

    def _set(self):
        """
        Set the wallpaper.
        """
        self.setter_type.set(self._file_path)
        if not self._disable_theme:
            self.wal.set(str(self._file_path))

    def _set_perma(self):
        """
        Set the wallpaper permanently
        """
        self.setter_type.set_perm(self._file_path)
        if not self._disable_theme:
            self.wal.save()

    def _is_exists(self):
        """
        Check if the wallpaper already exists.
        """
        return self._file_path.exists()

    def _blacklist(self, blacklist_obj):
        if not self.disable_blacklist:
            blacklist_obj.add_blacklist()

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
                self._blacklist(blacklist)
                self._restore()
                exit()
            elif ask.lower() == 'n':
                self._blacklist(blacklist)
                self._restore()
                remove(self._file_path)
