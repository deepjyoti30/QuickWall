"""All utility related functions defined here"""

import subprocess


def is_nitrogen():
    """
    Check if nitrogen is present or not
    """
    command = "nitrogen --help"
    p = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    ret, err = p.communicate()

    return True if err is None else False
