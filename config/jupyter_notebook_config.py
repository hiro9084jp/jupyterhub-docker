import os
import subprocess
from s3contents import S3ContentsManager
c = get_config()

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.terminals_enabled = False
c.NotebookApp.contents_manager_class = S3ContentsManager

c.S3ContentsManager.prefix = os.environ['JUPYTERHUB_USER']
c.S3ContentsManager.sse = "AES256"

keyfile = '/etc/jupyter/ssl.key'
certfile = '/etc/jupyter/ssl.crt'
subprocess.check_call([
    'openssl', 'req', '-new', '-newkey', 'rsa:2048', '-days', '3650', '-nodes', '-x509',
    '-subj', '/CN=selfsigned',
    '-keyout', keyfile,
    '-out', certfile,
])
c.NotebookApp.keyfile = keyfile
c.NotebookApp.certfile = certfile
