"""Functions related to usign feh as wallpaper setter."""

import subprocess
from pathlib import Path

from simber import Logger

# Declare the logger
logger = Logger("feh")


class feh:

    def __init__(self):
        self.feh_config_path = Path('~/.fehbg').expanduser()

        # Verify feh exists
        self.__verify_feh_bg_exists()

        self.current = self._find_current()

    def __verify_feh_bg_exists(self):
        """
        If feh is not run with `feh --bg-fill` even once before then the
        .fehbg file will not be present.

        Make a check to see if the file is present, and if not then raise an
        error asking the user to run it once.
        """
        if not self.feh_config_path.exists():
            logger.critical(
                ".fehbg does not exist. Seems like feh was never used before. Run feh using `feh --bg-fill <wallpaper_file>` and try again.")

    def _find_current(self):
        """
        Extract the current wall path.
        """
        logger.debug("{}".format(
            open(self.feh_config_path).read().split(' ')[-2]))
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
