#!/bin/bash

PROJECT_DIR="/full/path/to/your/project"
WATCH_DIR="/media/ieeegrp2/0403-0201/DCIM/100MEDIA"
PDF_SCRIPT="$PROJECT_DIR/PDF_Text.py"
C_PROGRAM="$PROJECT_DIR/BrailleAlphabet"
SPI_SCRIPT="$PROJECT_DIR/Brailly.py"

echo "Watching folder: $WATCH_DIR"

cd "$PROJECT_DIR" || exit 1

inotifywait -m -e close_write "$WATCH_DIR" --format '%f' | while read FILE
do
    FILEPATH="$WATCH_DIR/$FILE"

    if [ -f "$FILEPATH" ]; then
        echo "New file ready: $FILEPATH"

        python3 "$PDF_SCRIPT" "$FILEPATH"

        TXT_PATH="$(dirname "$FILEPATH")/neededtxt.txt"
        if [ ! -f "$TXT_PATH" ]; then
            echo "Error: neededtxt.txt was not created."
            continue
        fi

        "$C_PROGRAM" "$TXT_PATH"

        BRAILLE_PATH="$PROJECT_DIR/BrailleOutput.txt"
        if [ ! -f "$BRAILLE_PATH" ]; then
            echo "Error: BrailleOutput.txt was not created."
            continue
        fi

        python3 "$SPI_SCRIPT" "$BRAILLE_PATH"
    fi
done
