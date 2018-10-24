#!/bin/bash

git pull

sudo fuser -k 8000/tcp

cd /root/Bdbproject/bdbbuy_analysis/BdbbuyDataCenter
nohup python manage.py runserver 0.0.0.0:8000 >/dev/null 2>&1 &