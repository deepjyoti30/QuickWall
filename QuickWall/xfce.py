"""All code related to setting wallpaper in xfce is defined here."""

import os
from pathlib import Path
from bs4 import BeautifulSoup
from QuickWall.logger import Logger

logger = Logger("XFCE")


class XFCESetter:
    def __init__(self):
        self.cmd = "xfconf-query -c xfce4-desktop -p /backdrop/screen0/monitor0/workspace0/last-image -s {}"
        # Save the value of the previous wallpaper.
        self._extract_prev_wall()

    def _extract_prev_wall(self):
        """Extract the saved wallpaper from the xml file."""
        FILE = Path("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml").expanduser()
        try:
            soup = BeautifulSoup(open(FILE, 'r'))
            wall = soup.find("property", attrs={"name": "last-image"})
        except FileNotFoundError:
            logger.warning("{}: Not found. Wallpaper will not be restored!".format(FILE))
            return
        except Exception as e:
            logger.error("While extracting the wallpaper, error thrown: {}".format(e))
            return

        if wall == "":
            logger.warning("No value of last image. Wallpaper will not be restored!")
            return

        self.SAVED_WALL = wall.attrs['value']

    def set(self, wallpaper):
        """Set the wallpaper temporarily."""
        self.cmd.format(wallpaper)
        os.system(self.cmd)

    def set_perm(self, wallpaper):
        """Set the wallpaper permanently."""
        self.set(wallpaper)

    def restore(self):
        """Restore the saved wallpaper."""
        self.set_perm(self.SAVED_WALL)
