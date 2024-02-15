#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
import os
from fabric.api import local, env, put, run
from datetime import datetime


# Setup Fabric environment variables.
env.hosts = ['54.210.254.62', '54.227.96.209']
env.user = 'ubuntu'

def do_pack():
    """
    Return the archive path if the archive has been correctly packed or None otherwise
    """
    local('mkdir -p versions')
    now = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(now)

    archive = local('tar -cvzf {} web_static'.format(filename))

    if archive.succeeded:
        return filename
    else:
        return None
    
def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        new_version = '/data/web_static/releases/' + archived_file[:-4]

        archived_file = '/tmp/' + archived_file
        
        put(archive_path, '/tmp/')
        run('sudo mkdir -p {}'.format(new_version))

        run('sudo tar -xzf {} -C {}/'.format(archived_file,
                                        new_version))
        run('sudo rm {}'.format(archived_file))
        run('sudo mv {}/web_static/* {}/'.format(new_version,
                                                 new_version))
        
        # Clean up old releases
        run('sudo rm -rf {}/web_static'.format(new_version))
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s {} /data/web_static/current'.format(new_version))

        print('New version deployed!')
        return True
    else:
        return False