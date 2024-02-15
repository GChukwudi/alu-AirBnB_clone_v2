#!/usr/bin/env bash
# Sets up a web server for deployment of web_static.

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

echo "Holberton School" > /data/web_static/releases/test/index.html
ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

printf %s "server {
	listen 80 default_server;
	listen [::]:80 default_server;
	add_header X-Served-By $hostname;
	root /var/www/html;
	location /hbnb_static {
	    alias /data/web_static/current/;
	    index index.html index.htm;
	}
	
	location /redirect_me {
        return 301 http://github.com/GChukwudi;
	}
	
	error_page 404 /404.html;
	location /404 {
	    root /var/www/html;
	    internal;
	}
}" > /etc/nginx/site-available/default

ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
service nginx restart
