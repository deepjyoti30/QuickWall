"""Set the theme extracted from the wallpaper."""

from pywal import (
    colors, export, sequences, theme, settings
)
import os
from simber import Logger

logger = Logger("wal")


class Wal:
    """Change the theme based on the passed wallpaper"""

    def set(self, wallpaper):
        logger.debug("{}".format(wallpaper))
        self.colors_plain = colors.get(wallpaper)
        sequences.send(self.colors_plain, to_send=True)
        colors.palette()

    def save(self):
        export.every(self.colors_plain)

    def restore(self):
        self.colors_plain = theme.file(os.path.join(
            settings.CACHE_DIR,
            "colors.json"
        ))
        sequences.send(self.colors_plain, to_send=True)
