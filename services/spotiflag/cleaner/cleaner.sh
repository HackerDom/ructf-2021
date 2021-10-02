#!/bin/sh

if [ -z "$FOLDER" ]; then
    echo "Please, set \$FOLDER to continue."
    exit 1
fi

if [ -z "$EXPIRE" ]; then
    echo "Please, set \$EXPIRE to continue."
fi

PERIOD=${PERIOD:-60}

while true; do
    date -uR
    find "$FOLDER" -type f -and -not -newermt "-$EXPIRE seconds" -delete
    sleep "$PERIOD"
done
