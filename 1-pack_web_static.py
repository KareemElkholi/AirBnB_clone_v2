#!/usr/bin/python3
"""generates a .tgz archive from the contents of the web_static folder"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """return archive path"""
    local("mkdir -p versions")
    path = f"versions/web_static_{datetime.now().strftime('%Y%m%d%H%M%S')}.tgz"
    try:
        local(f"tar -cvzf {path} web_static")
        return path
    except Exception:
        return None
