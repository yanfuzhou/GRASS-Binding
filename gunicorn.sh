#!/bin/bash
WORK_NUM=4
source grass72.sh
source venv/bin/activate
gunicorn -w $WORK_NUM -k gevent -b 0.0.0.0:4000 grass_app:app