"""Setter related functions."""

from QuickWall.nitrogen import nitrogen
from QuickWall.feh import feh
from QuickWall.kde import KDEsetpaper
from QuickWall.xfce import XFCESetter
from QuickWall.logger import Logger
from QuickWall.utility import get_desktop_environment

# Declare the logger
logger = Logger("Setter")

LockscreenCompatibleSetters = ["kde"]


class WallSetter:
    """
    Select the wallpaper setter.
    """
    def __init__(self, setter_type, lockscreen=False):
        self.setter_type = setter_type
        self.available_setters = {
                                'nitrogen': nitrogen,
                                'feh': feh,
                                'kde': KDEsetpaper,
                                'xfce': XFCESetter
                                }
        self.setter = None
        self._select_setter()
        self.lockscreen = lockscreen

    def _detect_setter(self):
        DE = get_desktop_environment()
        logger.debug("Automatically detecting what setter to use.")
        logger.debug("Detected : {}".format(DE))
        if DE == "kde":
            return "kde"
        elif DE == "xfce4":
            return "xfce"
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

        if (self.lockscreen and self.setter_type in LockscreenCompatibleSetters):
            return self.setter(True)
        else:
            logger.warning("--set-lockscreen not available for the current wallpaper setter")

        return self.setter()
