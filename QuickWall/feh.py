"""Functions related to usign feh as wallpaper setter."""

import subprocess
from pathlib import Path

from simber import Logger

# Declare the logger
logger = Logger("feh")


class feh:

    def __init__(self):
        self.feh_config_path = Path('~/.fehbg').expanduser()
        self.current = self._find_current()

    def _find_current(self):
        """
        Extract the current wall path.
        """
        logger.debug("{}".format(open(self.feh_config_path).read().split(' ')[-2]))
        return open(self.feh_config_path).read().split(' ')[-2]

    def restore(self):
        """
        Restore the wallpaper
        """
        command = "feh --bg-fill {}".format(self.current)
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
