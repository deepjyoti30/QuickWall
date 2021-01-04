"""All code related to setting wallpaper in xfce is defined here."""

import os
from pathlib import Path
from bs4 import BeautifulSoup
from simber import Logger

logger = Logger("XFCE")


class XFCESetter:
    def __init__(self):
        self.cmd = "xfconf-query -c xfce4-desktop -p {wallpaper_image} -s {wallpaper}"
        # Save the value of the previous wallpaper.
        self._extract_prev_wall()

    def _extract_prev_wall(self):
        """Extract the saved wallpaper from the xml file."""
        FILE = Path("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml").expanduser()
        try:
            soup = BeautifulSoup(open(FILE, 'r'), features="html.parser")
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

    def _extract_workspace(self):
        """ Extract the monitor & wallpaper from the xml file"""
        FILE = Path("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml").expanduser()
        try:
            FILE = Path("~/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml").expanduser()
            soup = BeautifulSoup(open(FILE, 'r'), features="html.parser")
            base_find = soup.find_all("property", attrs={"name": "last-image", "type": "string"})
            monitors = [monitor.parent.parent["name"] for monitor in base_find]
            workspaces = [workspace.parent["name"] for workspace in base_find]
            if not len(list(monitors)) < 2:
                for idx, path in enumerate(zip(monitors, workspaces)):
                    path = "/backdrop/screen0/{monitor}/{workspace}/last-image".format(monitor=path[0], workspace=path[1])
                    print(idx, path)
                workspace = input("Which backdrop do you want to change? ")
                try:
                    workspace = int(workspace)
                except ValueError:
                    logger.info("You didn't type in a valid number, typed: {}" % workspace)
                return "/backdrop/screen0/{monitor}/{workspace}/last-image".format(monitor=monitors[workspace], workspace=workspaces[workspace])
            else:
                return "/backdrop/screen0/{monitor}/{workspace}/last-image".format(
                    monitor=monitors[0], workspace=workspaces[0])

        except FileNotFoundError:
            logger.warning("{}: Not found. Assuming default monitor!".format(FILE))
            return "/backdrop/screen0/monitor0/workspace0/last-image"
        except Exception as e:
            logger.error("While extracting the wallpaper, error thrown: {}. Assuming default monitor!".format(e))
            return "/backdrop/screen0/monitor0/workspace0/last-image"

    def set(self, wallpaper):
        """Set the wallpaper temporarily."""
        os.system(self.cmd.format(wallpaper=wallpaper, wallpaper_image=self._extract_workspace()))

    def set_perm(self, wallpaper):
        """Set the wallpaper permanently."""
        self.set(wallpaper)

    def restore(self):
        """Restore the saved wallpaper."""
        self.set_perm(self.SAVED_WALL)
