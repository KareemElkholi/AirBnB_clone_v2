#!/usr/bin/env bash
# sets up your web servers for the deployment
sudo su
apt update
apt install -y nginx
mkdir -p /data/web_static/shared/ /data/web_static/releases/test/
echo "test" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test /data/web_static/current
chown -R ubuntu:ubuntu /data/
sed -i "/listen 80 default_server;/a \\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n" /etc/nginx/sites-available/default
service nginx restart
