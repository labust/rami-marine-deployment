#!/bin/bash

# Provjeri je li broj argumenata točan
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <path_to_image> <output_csv>"
    exit 1
fi

# Postavi varijable
IMAGE_PATH="$1"
OUTPUT_CSV="$2"

# Pokreni Python skriptu s proslijeđenim argumentima
echo "Running pipeline.py with image: $IMAGE_PATH and output: $OUTPUT_CSV"
python3 pipeline.py "$IMAGE_PATH" "$OUTPUT_CSV"

# Provjeri je li Python skripta uspješno završila
if [ $? -eq 0 ]; then
    echo "Pipeline executed successfully."
else
    echo "Pipeline encountered an error."
    exit 2
fi
