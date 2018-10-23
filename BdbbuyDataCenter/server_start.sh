#!/bin/bash

sudo fuser -k 8000/tcp
python manager.py runserver 0.0.0.0:8000