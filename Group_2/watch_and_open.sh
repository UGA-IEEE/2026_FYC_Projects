#!/bin/bash

WATCH_DIR="/media/ieeegrp2/0403-0201/DCIM/100MEDIA"

echo "Watching folder: $WATCH_DIR"

inotifywait -m -e close_write "$WATCH_DIR" --format '%f' | while read FILE
do
    FILEPATH="$WATCH_DIR/$FILE"
    if [ -f "$FILEPATH" ]; then
        echo "New file ready: $FILEPATH"
        python3 /full/path/to/PDF_Text.py "$FILEPATH"
    fi
done
