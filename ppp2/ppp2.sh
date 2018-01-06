#!/bin/bash
# Simple starter script for all required sub components

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
MANAGE_PY=$DIR"/manage.py"

echo "Start Omnibus message server ..."
python3 $MANAGE_PY omnibusd &
OMNIBUSD=$!

echo "Start chat Bots ..."
python3 $MANAGE_PY startbots &
BOTS=$!

echo "Start HTTP server ..."
python3 $MANAGE_PY runserver 0.0.0.0:8000

echo "Shutdown ..."
kill $BOTS
kill $OMNIBUSD
