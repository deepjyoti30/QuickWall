"""Functions related to nitrogen."""

import subprocess

from simber import Logger

# Declare logger
logger = Logger("nitrogen")


class nitrogen:
    """
    Class to use nitrogen to set wallpapers.
    """
    def restore(self):
        """
        Restore the wallpaper using nitrogen.
        """
        logger.info("Restoring the last wallpaper...")
        c = 'nitrogen --restore'
        subprocess.Popen(c.split(), stdout=subprocess.PIPE)

    def set(self, file_path):
        """
        Set the wallpaper temporaririly
        """
        c = 'nitrogen --set-zoom-fill {}'.format(file_path)
        p = subprocess.Popen(c.split(' '), stdout=subprocess.PIPE)
        ret, err = p.communicate()

    def set_perm(self, file_path):
        """
        Set the wallpaper permanently.
        """
        c = 'nitrogen --save --set-zoom-fill {}'.format(file_path)
        subprocess.Popen(c.split(), stdout=subprocess.PIPE)
