from detekcija import process_image
from bartul.ocr_processing import process_ocr
from lucija.cr import color  # Funkcija za detekciju klase 1
import csv

def merge_pipeline(image_path, txt_data, output_csv):
    """
    Glavni pipeline koji integrira Lovrin, Bartulov i Lucijin dio.
    """
    try:
        # 1. Detekcija objekata (Lovrin model)
        detection_results = process_image(image_path)

        # 2. OCR prepoznavanje (Bartulov model)
        ocr_results = process_ocr(image_path, txt_data)

        # 3. Analiza boja za klasu 1 (Lucijin dio)
        class1_color = color(image_path, klasa=1)  # Dodavanje klase 1

        # Spajanje podataka prema klasi
        final_results = []
        for ocr_entry in ocr_results:
            for detection_entry in detection_results:
                if ocr_entry["class_id"] == detection_entry["class"]:  # Usporedba klasa
                    ocr_entry["centroid_x"] = detection_entry["cx"]
                    ocr_entry["centroid_y"] = detection_entry["cy"]

                    # Dodaj informacije o klasi 1 (ako je relevantno)
                    if detection_entry["class"] == 1:
                        ocr_entry["class1_color"] = class1_color

                    final_results.append(ocr_entry)
                    break

        # Generiranje CSV-a
        with open(output_csv, 'w', newline='') as f:
            fieldnames = ["timestamp", "class_id", "ocr_value", "centroid_x", "centroid_y", "class1_color"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_results)

        print(f"Pipeline completed. Output saved to {output_csv}")

    except Exception as e:
        print(f"Greška u pipeline-u: {e}")


# Primjer pokretanja pipeline-a
merge_pipeline(
    image_path="testnaSlika.jpg",
    txt_data="input.txt",
    output_csv="final_output.csv"
)
