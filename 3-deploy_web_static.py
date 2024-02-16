#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import local, env, put, run
from datetime import datetime
import os

env.hosts = ['54.210.254.62', '54.227.96.209']


def do_pack():
    """
    generates a .tgz archive
    """
    local('sudo mkdir -p versions')

    now = datetime.now()
    str_time = now.strftime("%Y%m%d%H%M%S")

    local('sudo tar -cvzf versions/web_static_{}.tgz \
          web_static'.format(str_time))
    return "versions/web_static_{}.tgz".format(str_time)


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if os.path.exists(archive_path) is False:
        return False
    try:
        file_n = archive_path.split("/")[-1]
        file_p = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}{}/".format(path, file_p))
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(file_n, path, file_p))
        run("sudo rm /tmp/{}".format(file_n))
        run("sudo mv -n {0}{1}/web_static/* {0}{1}/".format(path, file_p))
        run("sudo rm -rf {}{}/web_static".format(path, file_p))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(path, file_p))
        return True
    except:
        return False


def deploy():
    """
    creates and distributes an archive to your web servers
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(path)
