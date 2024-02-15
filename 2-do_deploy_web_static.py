#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
import os
from fabric.api import local, env, put, run


env.hosts = ['54.210.254.62', '54.227.96.209']
env.user = 'ubuntu'

@task
def do_pack():
    """
    Return the archive path if the archive has been correctly packed or None otherwise
    """
    local('mkdir -p versions')
    result = local('tar -cvzf versions/web_static_$(date "+%Y%m%d%H%M%S").tgz web_static')
    if result.failed:
        return None
    else:
        return result
    
def do_deploy(archive_path):
    """
    Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, '/tmp/')
        archive_name = archive_path.split('/')[1]
        archive_name_no_ext = archive_name.split('.')[0]
        run('mkdir -p /data/web_static/releases/{}'.format(archive_name_no_ext))
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}'.format(archive_name, archive_name_no_ext))
        run('rm /tmp/{}'.format(archive_name))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{} /data/web_static/current'.format(archive_name_no_ext))
        return True
    except:
        return False
    return False
    