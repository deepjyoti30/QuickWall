"""Set wallpapers in KDE."""

import dbus
from os import path, system
from shutil import copy

from QuickWall.logger import Logger
logger = Logger("nitrogen")


def setwallpaper(filepath):
    """
    This script is taken from https://github.com/pashazz/ksetwallpaper/

    All the credit goes to the user for the code, I'm just using it
    to add a functionality to my app.
    """

    jscript = """var allDesktops = desktops();
    for ( i = 0; i < allDesktops.length;i++ ) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", "file://%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % filepath)


def saveRestorableWallpaper():
    """
    Save current wallpaper as RestorableImage in kde wallpaper config 
    """
    jscript = """var first = desktopForScreen(0);
    first.currentConfigGroup = Array( 'Wallpaper', 'org.kde.image', 'General' );
    var img = first.readConfig('Image');
    first.writeConfig('RestorableImage' , img);
    """

    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript)


def restoreWallpaper():
    """
    Load wallpaper from RestorableImage config
    """
    jscript = """var first = desktopForScreen(0);
    first.currentConfigGroup = Array( 'Wallpaper', 'org.kde.image', 'General' );
    var img = first.readConfig('RestorableImage');
    var allDesktops = desktops();
    for ( i = 0; i < allDesktops.length;i++ ) {
        d = allDesktops[i];
        d.wallpaperPlugin = "org.kde.image";
        d.currentConfigGroup = Array("Wallpaper", "org.kde.image", "General");
        d.writeConfig("Image", img)
    }
    """

    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript)


class KDEsetpaper:
    def __init__(self):
        """Initialize KDE workflow"""
        saveRestorableWallpaper()

    def set(self, file_path):
        """Set wallpaper"""
        setwallpaper(file_path)

    def set_perm(self, file_path):
        """
        Permanetly set wallpaper.

        Creates restorableImage.jpg which allows kde to
        restore image as it doesnt store images by itself.
        """
        new_path = path.dirname(file_path) + "/restorableImage.jpg"
        copy(file_path, new_path)
        setwallpaper(new_path)

        ask = input("Do you want to set lockscreen wallpaper ? [Y]es [N]o ")
        if (ask.lower() == "y"):
            # Set lock screen as wallpaper
            # Based on https://github.com/RaitaroH/KDE-Terminal-Wallpaper-Changer

            command = "kwriteconfig5 --file kscreenlockerrc --group Greeter --group Wallpaper --group org.kde.image --group General --key Image \"file://{}\"".format(new_path)
            system(command)

    def restore(self):
        """Restore wallpaper"""
        logger.info("Restoring the last wallpaper...")
        restoreWallpaper()
