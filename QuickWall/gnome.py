import subprocess
from pathlib import Path
from QuickWall.logger import Logger

logger = Logger("GNOME")


class GNOMESetter:
    def __init__(self):
        self.cmd = "gsettings set org.gnome.desktop.background picture-uri file://{wallpaper}"
        self._extract_prev_wall()

    def _extract_prev_wall(self):
        """Extract the saved wallpaper from the cmd line."""
        self.SAVED_WALL = subprocess.check_output(["gsettings", "get", "org.gnome.desktop.background", "picture-uri"])[1:-2].decode('utf-8')

    def set(self, wallpaper):
        """Set the wallpaper temporarily."""
        subprocess.call(self.cmd.format(wallpaper=wallpaper).split(" "))

    def set_perm(self, wallpaper):
        """Set the wallpaper permanently."""
        self.set(wallpaper)

    def restore(self):
        """Restore the saved wallpaper."""
        self.set_perm(self.SAVED_WALL)