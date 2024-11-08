#!/bin/bash

# Arguments: input image path and output directory
INPUT_IMAGE=$1
OUTPUT_DIR=$2

# Ensure output directory exists
mkdir -p $OUTPUT_DIR

# Step 1: Run Object Detection
echo "Running Object Detection..."
python object_detection.py $INPUT_IMAGE $OUTPUT_DIR

# Step 2: Run OCR on Detected Regions
echo "Running OCR..."
python ocr_processing.py "$OUTPUT_DIR/detections.json" $OUTPUT_DIR

# Step 3: Generate Final Output CSV
echo "Generating Final Output..."
python generate_final_output.py "$OUTPUT_DIR/ocr_results.json" "$OUTPUT_DIR/final_output.csv"

echo "Pipeline completed. Final output saved to $OUTPUT_DIR/final_output.csv"
