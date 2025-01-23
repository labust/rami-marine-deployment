from ..Lucija.cr import color  # Lucijin model za analizu boja
from ..Lovre.detekcija import process_image  # Lovrin model za detekciju objekata
from ..OCR.ocr_script import process_ocr  # Bartulov OCR model
import csv

def merge_pipeline(image_path, ocr_model_dir, output_csv):
    """
    Glavni pipeline za integraciju svih komponenti.
    """
    try:
        # 1. Detekcija objekata (Lovrin model)
        detection_results = process_image(image_path)

        # 2. OCR prepoznavanje (Bartulov model)
        ocr_results = []
        for det in detection_results:
            if "crop" in det:  # Ako je dostupan crop
                ocr_value = process_ocr(det["crop"], model_dir=ocr_model_dir)
                det["ocr_value"] = ocr_value
                ocr_results.append(det)

        # 3. Analiza boja za klasu 1 (Lucijin model)
        for det in detection_results:
            if det["class"] == 1:
                det["instance"] = color(image_path, klasa=1)
            else:
                det["instance"] = "N/A"

        # Generiranje CSV-a
        with open(output_csv, 'w', newline='') as f:
            fieldnames = ["timestamp", "class", "instance", "centroid_x", "centroid_y"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for det in detection_results:
                writer.writerow({
                    "timestamp": det["timestamp"],
                    "class": det["class"],
                    "instance": det["instance"],
                    "centroid_x": det["cx"],
                    "centroid_y": det["cy"]
                })

        print(f"Pipeline completed. Output saved to {output_csv}")

    except Exception as e:
        print(f"Greška u pipeline-u: {e}")
