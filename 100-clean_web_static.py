#!/usr/bin/python3
"""
Fabric script that deletes out-of-date archives
"""
from fabric.api import env, run, local
from datetime import datetime
from fabric.context_managers import lcd, cd

env.hosts = ['54.90.67.236', '54.90.237.122']
env.user = "ubuntu"


def do_clean(number=0):
    """
    Deletes out-of-date archives
    """
    number = int(number)
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    # Local clean
    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number))

    # Remote clean
    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number))
    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number))
    return True
