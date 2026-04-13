#!/bin/bash

PROJECT_DIR="/documents/2026_FYC_Projects/Group_2"
WATCH_DIR="/media/ieeegrp2/0403-0201/DCIM/100MEDIA"
PDF_SCRIPT="$PROJECT_DIR/PDF_Text.py"
C_PROGRAM="$PROJECT_DIR/BrailleAlphabet"
I2C_SCRIPT="$PROJECT_DIR/i2c_driver.py"

echo "Watching folder: $WATCH_DIR"

cd "$PROJECT_DIR" || exit 1

inotifywait -m -e close_write "$WATCH_DIR" --format '%f' | while read FILE
do
    FILEPATH="$WATCH_DIR/$FILE"

    if [ -f "$FILEPATH" ]; then
        echo "New file ready: $FILEPATH"

        # Step 1: Extract text from PDF
        python3 "$PDF_SCRIPT" "$FILEPATH"

        TXT_PATH="$(dirname "$FILEPATH")/neededtxt.txt"
        if [ ! -f "$TXT_PATH" ]; then
            echo "Error: neededtxt.txt was not created."
            continue
        fi

        # Step 2: Convert text to braille binary
        "$C_PROGRAM" "$TXT_PATH"

        BRAILLE_PATH="$PROJECT_DIR/BrailleOutput.txt"
        if [ ! -f "$BRAILLE_PATH" ]; then
            echo "Error: BrailleOutput.txt was not created."
            continue
        fi

        # Step 3: Send braille binary to TPIC2810 over I2C
        python3 "$I2C_SCRIPT" "$BRAILLE_PATH"
    fi
done    fi
done
