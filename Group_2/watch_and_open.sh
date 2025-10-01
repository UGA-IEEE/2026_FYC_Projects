#!/bin/bash

WATCH_DIR="/media/ieeegrp2/0403-0201/DCIM/100MEDIA"

echo "Watching folder: $WATCH_DIR"

inotifywait -m -e create "$WATCH_DIR" --format '%f' | while read FILE
do
    FILEPATH="$WATCH_DIR/$FILE"
    echo "New file detected: $FILEPATH"
    code "$FILEPATH"
done
