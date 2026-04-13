#!/bin/bash

PROJECT_DIR="/documents/2026_FYC_Projects/Group_2"
WATCH_DIR="/media/ieeegrp2/0403-0201/DCIM/100MEDIA"
PIPELINE_SCRIPT="$PROJECT_DIR/master_pipeline.py"

echo "Watching folder: $WATCH_DIR"

cd "$PROJECT_DIR" || exit 1

inotifywait -m -e close_write "$WATCH_DIR" --format '%f' | while read FILE
do
    FILEPATH="$WATCH_DIR/$FILE"

    if [[ "$FILEPATH" != *.pdf ]]; then
        echo "Skipping non-PDF file: $FILEPATH"
        continue
    fi

    if [ -f "$FILEPATH" ]; then
        echo "----------------------------------------"
        echo "New PDF detected: $FILEPATH"
        echo "Running master pipeline..."

        python3 "$PIPELINE_SCRIPT" "$FILEPATH"

        if [ $? -eq 0 ]; then
            echo "Pipeline completed successfully."
        else
            echo "Pipeline failed."
        fi

        echo "Finished processing: $FILEPATH"
        echo "----------------------------------------"
    fi
done
