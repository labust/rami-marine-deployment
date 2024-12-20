import json
import csv
import time

def dummy_pipeline(detection_path, ocr_path, output_csv):
    # Učitavanje podataka
    with open(detection_path, 'r') as f:
        detections = json.load(f)
    with open(ocr_path, 'r') as f:
        ocr_results = json.load(f)

    # Spajanje OCR rezultata s detekcijama
    results = []
    timestamp = int(time.time())
    for detection in detections:
        for ocr in ocr_results:
            if detection["bbox"] == ocr["bbox"]:  # Usporedba bounding boxova
                centroid_x = (detection["bbox"][0] + detection["bbox"][2]) // 2
                centroid_y = (detection["bbox"][1] + detection["bbox"][3]) // 2
                results.append({
                    "timestamp": timestamp,
                    "class": detection["class"],
                    "instance": ocr["text"],
                    "centroid_x": centroid_x,
                    "centroid_y": centroid_y
                })

    # Generiranje CSV-a
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ["timestamp", "class", "instance", "centroid_x", "centroid_y"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"Pipeline završen. Rezultati spremljeni u {output_csv}")
