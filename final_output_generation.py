import json
import csv
import os
import time

def generate_final_output(ocr_json_path, output_csv_path):
    # Load OCR results
    with open(ocr_json_path, 'r') as json_file:
        ocr_results = json.load(json_file)
    
    # Open CSV file for writing
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['timestamp', 'class', 'instance', 'centroid_x', 'centroid_y']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        # Get current timestamp for results
        timestamp = int(time.time())
        
        # Write results to CSV
        for result in ocr_results:
            label = result["label"]
            text = result["text"]
            bbox = result["bbox"]
            x = bbox[0] + bbox[2] // 2  # Calculate centroid x
            y = bbox[1] + bbox[3] // 2  # Calculate centroid y
            
            writer.writerow({
                "timestamp": timestamp,
                "class": label,
                "instance": text,
                "centroid_x": x,
                "centroid_y": y
            })
    
    print(f"Final output generated and saved to {output_csv_path}")

if __name__ == "__main__":
    import sys
    ocr_json_path = sys.argv[1]
    output_csv_path = sys.argv[2]
    generate_final_output(ocr_json_path, output_csv_path)
