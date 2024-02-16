#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
import os
from fabric.api import env, put, run
from datetime import datetime

# Setup Fabric environment variables.
env.hosts = ['54.210.254.62', '54.227.96.209']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        file_p = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}{}/".format(path, file_p))
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(file_n, path, file_p))
        run("sudo rm /tmp/{}".format(file_n))
        run("sudo mv {0}{1}/web_static/* {0}{1}/".format(path, file_p))
        run("sudo rm -rf {}{}/web_static".format(path, file_p))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(path, file_p))
        return True
    except:
        return False
