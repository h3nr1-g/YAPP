#!/bin/bash

SRC_DIR="/root/yapp"

if [ ! -f "$SRC_DIR/db/db.sqlite3" ]; then
    cp "$SRC_DIR/db.sqlite3" "$SRC_DIR/db/db.sqlite3"
fi

echo "Start Django application"
gunicorn --workers 3 \
         --chdir $SRC_DIR \
         --access-logfile - \
         --bind 0.0.0.0:8000 \
         yapp.wsgi
