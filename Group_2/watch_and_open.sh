#!/bin/bash
WATCH_DIR="/media/ieeegrp2/0403-0201/DCIM/100MEDIA"

echo "Watching folder: $WATCH_DIR"

inotifywait -m -e close_write,moved_to --format '%f' "$WATCH_DIR" | while read -r FILE
do
  FILEPATH="$WATCH_DIR/$FILE"
  [[ "$FILE" != *.pdf ]] && continue

  echo "Processing: $FILEPATH"
  python3 /path/to/pdf_text_extractor.py "$FILEPATH"
done
