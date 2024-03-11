#!/usr/bin/python3
"""configuring servers"""
from fabric.api import env, put, sudo, local
from datetime import datetime
from os.path import exists
env.hosts = ['54.174.219.233', '35.153.78.199']


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder"""
    local("mkdir -p versions")
    path = f"versions/web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    try:
        local(f"tar -cvzf {path} web_static")
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """distributes an archive to web servers"""
    if exists(archive_path):
        try:
            file = archive_path.split('/')[-1]
            path = f"/data/web_static/releases/{file.split('.')[0]}"
            put(archive_path, '/tmp/')
            sudo(f'mkdir -p {path}')
            sudo(f'tar -xzf /tmp/{file} -C {path}')
            sudo(f'rm /tmp/{file}')
            sudo(f'rsync -a {path}/web_static {path}')
            sudo(f'rm -rf {path}/web_static')
            sudo('rm -rf /data/web_static/current')
            sudo(f'ln -s {path} /data/web_static/current')
            return True
        except Exception:
            return False
    else:
        return False
