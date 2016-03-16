#!/bin/bash

. /home/app/imageserver/venv/bin/activate & gunicorn -b 0.0.0.0:80 imageserver:application &
