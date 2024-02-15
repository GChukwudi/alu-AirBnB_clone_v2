#!/usr/bin/python3
# Write a Fabric script (based on the file 1-pack_web_static.py) that distributes an archive to your web servers, using the function do_deploy:

# Prototype: def do_deploy(archive_path):
# Returns False if the file at the path archive_path doesn’t exist
# The script should take the following steps:
# Upload the archive to the /tmp/ directory of the web server
# Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension> on the web server
# Delete the archive from the web server
# Delete the symbolic link /data/web_static/current from the web server
# Create a new the symbolic link /data/web_static/current on the web server, linked to the new version of your code (/data/web_static/releases/<archive filename without extension>)
# All remote commands must be executed on your both web servers (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
# Returns True if all operations have been done correctly, otherwise returns False
# You must use this script to deploy it on your servers: xx-web-01 and xx-web-02
# In the following example, the SSH key and the username used for accessing to the server are passed in the command line. Of course, you could define them as Fabric environment variables (ex: env.user =...)

# Disclaimer: commands execute by Fabric displayed below are linked to the way we implemented the archive function do_pack - like the mv command - depending of your implementation of it, you may don’t need it

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
    