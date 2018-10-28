#!/bin/bash

sudo fuser -k 8000/tcp
nohup python manage.py runserver 0.0.0.0:8000 >/dev/null 2>&1 &