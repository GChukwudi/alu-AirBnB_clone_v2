#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
import os
from fabric.api import env, put, run, local
from datetime import datetime

# Setup Fabric environment variables.
env.hosts = ['54.210.254.62', '54.227.96.209']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    """
    local('sudo mkdir -p versions')

    now = datetime.now()
    str_time = now.strftime("%Y%m%d%H%M%S")

    local('sudo tar -cvzf versions/web_static_{}.tgz \
          web_static'.format(str_time))

    return 'versions/web_static_{}.tgz'.format(str_time)

def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        print("Archive file doesn't exist.")
        return False

    try:
        archived_file = archive_path.split('/')[-1]
        new_version = '/data/web_static/releases/' + archived_file[:-4]

        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}'.format(new_version))
        run('sudo tar -xzf /tmp/{} -C {}'.format(archived_file, new_version))
        run('sudo rm /tmp/{}'.format(archived_file))
        run('sudo mv {}/web_static/* {}'.format(new_version, new_version))
        run('sudo rm -rf {}/web_static'.format(new_version))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(new_version))

        print('New version deployed!')
        return True
    except Exception as e:
        print("Error deploying: {}".format(str(e)))
        return False
