"""All utility related functions defined here"""

import subprocess

from pathlib import Path
from shutil import rmtree
from os import mkdir, path, environ
from sys import platform
from distutils.dir_util import copy_tree

from QuickWall.logger import Logger


# Declare logger
logger = Logger("Utility")


def is_nitrogen():
    """
    Check if nitrogen is present or not
    """
    command = "nitrogen --help"
    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    ret, err = p.communicate()

    return True if err is None else False


def is_feh():
    """
    Check if feh is installed.
    """
    command = "feh --help"

    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    ret, err = p.communicate()

    return True if err is None else False


def clear_cache(dir="~/.cache/QuickWall"):
    """
    Clear the cache from the QuickWall dir
    """
    dir_path = Path(dir).expanduser()
    logger.info("Removing {}".format(dir_path))

    if dir_path.exists():
        rmtree(dir_path)
        mkdir(dir_path)
    else:
        logger.warning("{}: Does not exist".format(dir))


def migrate_to_new_loc():
    """Move the files from the older dir to the new cache location."""
    src = path.expanduser("~/.QuickWall")
    des = path.expanduser("~/.cache/QuickWall")

    copy_tree(src, des)

    rmtree(src, ignore_errors=True)


def get_desktop_environment():
    # From http://stackoverflow.com/questions/2035657/what-is-my-current-desktop-environment
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=652320
    # and http://ubuntuforums.org/showthread.php?t=1139057
    if platform in ["win32", "cygwin"]:
        return "windows"
    elif platform == "darwin":
        return "mac"
    else:
        # Most likely either a POSIX system or something not much common
        desktop_session = environ.get("DESKTOP_SESSION")

        # easier to match if we doesn't have to deal with caracter cases
        if desktop_session is not None:
            desktop_session = desktop_session.lower()
            if desktop_session in [
                    "gnome",
                    "unity",
                    "cinnamon",
                    "mate",
                    "xfce4",
                    "lxde",
                    "fluxbox",
                    "blackbox",
                    "openbox",
                    "icewm",
                    "jwm",
                    "afterstep",
                    "trinity",
                    "kde",
                    "i3"
            ]:
                return desktop_session
            # # Special cases # #
            # Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
            # There is no guarantee that they will not do the same with the other desktop environments.
            elif "xfce" in desktop_session or desktop_session.startswith("xubuntu"):
                return "xfce4"
            elif desktop_session.startswith("ubuntu"):
                return "unity"
            elif desktop_session.startswith("lubuntu"):
                return "lxde"
            elif desktop_session.startswith("kubuntu"):
                return "kde"
            elif desktop_session.startswith("razor"):  # e.g. razorkwin
                return "razor-qt"
            elif desktop_session.startswith("wmaker"):  # e.g. wmaker-common
                return "windowmaker"
        if environ.get('KDE_FULL_SESSION') == 'true':
            return "kde"
        elif environ.get('GNOME_DESKTOP_SESSION_ID'):
            if "deprecated" not in environ.get('GNOME_DESKTOP_SESSION_ID'):
                return "gnome2"
        # From http://ubuntuforums.org/showthread.php?t=652320
        elif self.is_running("xfce-mcs-manage"):
            return "xfce4"
        elif self.is_running("ksmserver"):
            return "kde"
    return "unknown"
