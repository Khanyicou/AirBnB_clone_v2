```python
#!/usr/bin/python3
# Fabfile to create and distribute an archive to a web server.
import os.path
from datetime import datetime
from fabric import Connection, task

env = Connection("user@server")  # Update with your user and server details

def do_pack():
    """Create a tar gzipped archive of the directory web_static."""
    dt = datetime.utcnow()
    file = f"versions/web_static_{dt.strftime('%Y%m%d%H%M%S')}.tgz"
    if not os.path.isdir("versions"):
        os.makedirs("versions")
    result = local("tar -cvzf {} web_static".format(file), capture=True)
    if result.failed:
        return None
    return file

@task
def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    if not os.path.isfile(archive_path):
        return False
    file = os.path.basename(archive_path)
    name = file.split(".")[0]

    result = env.put(archive_path, f"/tmp/{file}")
    if result.failed:
        return False

    commands = [
        f"rm -rf /data/web_static/releases/{name}/",
        f"mkdir -p /data/web_static/releases/{name}/",
        f"tar -xzf /tmp/{file} -C /data/web_static/releases/{name}/",
        f"rm /tmp/{file}",
        f"mv /data/web_static/releases/{name}/web_static/* "
        f"/data/web_static/releases/{name}/",
        f"rm -rf /data/web_static/releases/{name}/web_static",
        f"rm -rf /data/web_static/current",
        f"ln -s /data/web_static/releases/{name}/ /data/web_static/current"
    ]

    for command in commands:
        result = env.run(command)
        if result.failed:
            return False
    return True

@task
def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
