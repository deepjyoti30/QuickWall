"""Functions related to usign feh as wallpaper setter."""

import subprocess

from QuickWall.logger import Logger

# Declare the logger
logger = Logger("feh")


class feh:

    def restore(self):
        """
        Restore the wallpaper
        """
        command = "sh ~/.fehbg"
        subprocess.Popen(command.split(), stdout=subprocess.PIPE)

    def set(self, file_path):
        """
        Set the wallpaper temporarily.
        """
        command = "feh --bg-fill {}".format(file_path)
        p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
        ret, err = p.communicate()

    def set_perm(self, file_path):
        """
        Set the wallpaper permanently.
        """
        self.set(file_path)
