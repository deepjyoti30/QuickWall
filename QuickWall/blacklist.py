"""All blacklist related functions."""

from pathlib import Path

from QuickWall.logger import Logger

# Declare logger
logger = Logger("blacklist")


class Blacklist:
    """
    Functions to be used related to blacklist.
    """
    def __init__(self, unique_id):
        self.blacklist_path = Path('~/.cache/QuickWall/blacklist').expanduser()
        self.unique_id = unique_id

    def is_blacklisted(self):
        """
        Check if the passed unique_id is available in the blacklist.
        """

        if not self.blacklist_path.exists():
            return False

        blacklist = open(self.blacklist_path).read().split('\n')[1:]

        logger.debug(str(blacklist))

        if self.unique_id in blacklist:
            return True
        else:
            return False

    def add_blacklist(self, silent=False):
        """
        Add the passed unique_id to blacklist.
        """
        if not self.blacklist_path.exists():
            open(self.blacklist_path, 'w')

        WRITESTREAM = open(self.blacklist_path, 'a+')
        WRITESTREAM.write('\n{}'.format(self.unique_id))

        if not silent:
            logger.info("{} added to blacklist".format(self.unique_id))

    def remove_blacklist(self):
        """Remove the passed id from the file."""
        if not self.blacklist_path.exists():
            return

        black_list = open(self.blacklist_path, 'r').read()
        black_list = black_list.split('\n')

        if self.unique_id in black_list:
            black_list.remove(self.unique_id)
            logger.info("Removed {} from the blacklist".format(self.unique_id))
        else:
            logger.critical("[{}] not available in the blacklist.".format(self.unique_id))

        black_list = '\n'.join(black_list)
        open(self.blacklist_path, 'w').write(black_list)
