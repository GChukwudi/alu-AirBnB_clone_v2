#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    """
    local('sudo mkdir -p versions')

    now = datetime.now()
    str_time = now.strftime("%Y%m%d%H%M%S")
    # print(str_time)

    local('sudo tar -cvzf versions/web_static_{}.tgz \
          web_static'.format(str_time))
