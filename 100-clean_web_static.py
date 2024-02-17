#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
import os
from fabric.api import *

env.hosts = ['54.90.67.236', '54.90.237.122']


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = 1 if int(number) == 0 else int(number)

    archives = sorted(os.listdir("versions"))
    [archives.pop() for i in range(number)]

    with lcd("versions"):
        [local("rm -f {}".format(archive)) for archive in archives]

    with cd("/data/web_static/releases"):
        archives = run("ls -tr").split()
        archives = [archive for archive in archives if "web_static_" \
                     in archive]
        [archives.pop() for i in range(number)]

        # Remove the same version of application from both directories
        [run("rm -rf ./{}".format(archive)) for archive in archives]
