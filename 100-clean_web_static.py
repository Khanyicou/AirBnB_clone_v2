#!/usr/bin/python3
# Fabfile to delete out-of-date archives.
import os
from fabric.api import *

env.hosts = ["104.196.168.90", "35.196.46.172"]


def do_clean(number=1):
    """Delete out-of-date archives.

    Args:
        number (int): The number of archives to keep.

    If number is 0 or 1, keeps only the most recent archive. If
    number is 2, keeps the most and second-most recent archives,
    etc.
    """
    number = int(number)

    # Ensure we keep at least one archive
    if number < 1:
        number = 1

    with lcd("versions"):
        # List all archives sorted by modification time
        archives = sorted(os.listdir("."), key=os.path.getmtime)

        # Remove all but the 'number' most recent archives
        for archive in archives[:-number]:
            local("rm -f {}".format(archive))

    with cd("/data/web_static/releases"):
        # List all archives sorted by modification time
        archives = run("ls -tr | grep web_static_").split()

        # Remove all but the 'number' most recent archives
        for archive in archives[:-number]:
            run("rm -rf {}".format(archive))

