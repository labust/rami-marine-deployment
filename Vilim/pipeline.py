from lovre.object_detection import detect_objects
from bartul.ocr_processing import process_ocr
import csv

def merge_pipeline(output_csv):
    # Poziv funkcija iz Lovrinog i Bartulovog koda
    detection_results = detect_objects()
    ocr_results = process_ocr()

    # Spajanje podataka prema class_id
    for ocr_entry in ocr_results:
        for detection_entry in detection_results:
            if ocr_entry["class_id"] == detection_entry["class_id"]:
                ocr_entry["generic_x"] = detection_entry["x_center"]
                ocr_entry["generic_y"] = detection_entry["y_center"]
                break

    # Generiranje CSV-a
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ["timestamp", "class_id", "ocr_value", "centroid_x", "centroid_y"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in ocr_results:
            writer.writerow({
                "timestamp": entry["timestamp"],
                "class_id": entry["class_id"],
                "ocr_value": entry["ocr_value"],
                "centroid_x": entry["generic_x"],
                "centroid_y": entry["generic_y"]
            })

    print(f"Pipeline completed. Output saved to {output_csv}")


# Primjer pokretanja
if __name__ == "__main__":
    merge_pipeline("final_output.csv")
