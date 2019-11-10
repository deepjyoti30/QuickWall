"""Setter related functions."""

from QuickWall.nitrogen import nitrogen
from QuickWall.feh import feh
from QuickWall.kde import KDEsetpaper
from QuickWall.logger import Logger
from QuickWall.utility import get_desktop_environment

# Declare the logger
logger = Logger("Setter")


class WallSetter:
    """
    Select the wallpaper setter.
    """
    def __init__(self, setter_type):
        self.setter_type = setter_type
        self.available_setters = {
                                'nitrogen': nitrogen,
                                'feh': feh,
                                'kde': KDEsetpaper,
                                }
        self.setter = None
        self._select_setter()

    def _detect_setter(self):
        DE = get_desktop_environment()
        logger.debug("Automatically detecting what setter to use.")
        if DE == "kde":
            return "kde"
        elif DE in [
                "i3",
                "unknown",
                ]:
            return "nitrogen"

    def _select_setter(self):
        """Select the wallpaper setter."""
        if self.setter_type == "auto":
            self.setter_type = self._detect_setter()

        try:
            self.setter = self.available_setters[self.setter_type]
        except KeyError:
            logger.critical("Passed wallpaper setter is not supported yet!\a")

    def get_setter(self):
        """
        Return the setter.
        """
        logger.info("Using {} as wallpaper setter".format(self.setter_type))
        return self.setter()
