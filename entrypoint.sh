#!/usr/bin/env bash
set -euo pipefail

sed -i -e "s%__JPYNB_S3_ACCESS_KEY_ID__%${JPYNB_S3_ACCESS_KEY_ID}%g" /usr/local/etc/jupyter/jupyter_notebook_config.py
sed -i -e "s%__JPYNB_S3_SECRET_ACCESS_KEY__%${JPYNB_S3_SECRET_ACCESS_KEY}%g" /usr/local/etc/jupyter/jupyter_notebook_config.py
sed -i -e "s%__JPYNB_S3_REGION_NAME__%${JPYNB_S3_REGION_NAME}%g" /usr/local/etc/jupyter/jupyter_notebook_config.py
sed -i -e "s%__JPYNB_S3_BUCKET_NAME__%${JPYNB_S3_BUCKET_NAME}%g" /usr/local/etc/jupyter/jupyter_notebook_config.py

rsync -auzv /usr/local/etc/jupyter/ /etc/jupyter/

# hub_ip is the interface that the hub listens on, 0.0.0.0 == all
# hub_connect_ip is the IP that _other_ services will connect to the hub on, i.e. the current private IP address
jupyterhub --config=/etc/jupyter/jupyterhub_config.py --JupyterHub.hub_ip="0.0.0.0" --JupyterHub.hub_connect_ip="$(curl -Lfs http://169.254.169.254/latest/meta-data/local-ipv4)"
