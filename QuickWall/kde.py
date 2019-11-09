"""Set wallpapers in KDE."""

import dbus


def setwallpaper(filepath, plugin='org.kde.image'):
    """
    This script is taken from https://github.com/pashazz/ksetwallpaper/

    All the credit goes to the user for the code, I'm just using it
    to add a functionality to my app.
    """

    jscript = """
    var allDesktops = desktops();
    print (allDesktops);
    for (i=0;i<allDesktops.length;i++) {
        d = allDesktops[i];
        d.wallpaperPlugin = "%s";
        d.currentConfigGroup = Array("Wallpaper", "%s", "General");
        d.writeConfig("Image", "file://%s")
    }
    """
    bus = dbus.SessionBus()
    plasma = dbus.Interface(bus.get_object('org.kde.plasmashell', '/PlasmaShell'), dbus_interface='org.kde.PlasmaShell')
    plasma.evaluateScript(jscript % (plugin, plugin, filepath))


class KDEsetpaper:
    """Use the script available in ./utils to set the wall."""
    def set(self, file_path):
        setwallpaper(file_path)

    def set_perm(self, file_path):
        # Same as set
        self.set(file_path)

    def restore(self):
        """Currently there is no way to restore the last wallpaper."""
        pass
