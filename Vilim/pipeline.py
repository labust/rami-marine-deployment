from detekcija import process_image
from bartul.ocr_processing import process_ocr
import csv

def merge_pipeline(image_path, txt_data, output_csv):
    # Koristi detekciju iz Lovrinog modela
    detection_results = process_image(image_path)

    # Koristi OCR iz Bartulovog modela
    ocr_results = process_ocr(image_path, txt_data)

    # Spajanje podataka prema klasi
    final_results = []
    for ocr_entry in ocr_results:
        for detection_entry in detection_results:
            if ocr_entry["class_id"] == detection_entry["class"]:  # Usporedba klasa
                ocr_entry["centroid_x"] = detection_entry["cx"]
                ocr_entry["centroid_y"] = detection_entry["cy"]
                final_results.append(ocr_entry)
                break

    # Generiraj CSV
    with open(output_csv, 'w', newline='') as f:
        fieldnames = ["timestamp", "class_id", "ocr_value", "centroid_x", "centroid_y"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_results)

    print(f"Pipeline completed. Output saved to {output_csv}")

# Primjer poziva pipeline-a
merge_pipeline("testnaSlika.jpg", "input.txt", "final_output.csv")
