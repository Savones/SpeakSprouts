#!/bin/bash

SERVICE="speak-sprouts"

if [ "$1" == "systemd" ]; then
    systemctl --user $2 "$SERVICE"
elif [ "$1" == "update" ]; then
    git fetch origin
    if $(git pull | grep -q '^Updating'); then
        systemctl --user daemon-reload
        systemctl --user restart "$SERVICE"
    fi
else
    source venv/bin/activate
    source .env
    flask run --host=$HOST --port=$PORT
fi
