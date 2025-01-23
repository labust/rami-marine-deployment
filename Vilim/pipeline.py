from Lovre.zavrsnaSkripta.detekcija import process_image
from OCR.ocr_script import process_ocr
from Lucija.cr import color  # Funkcija za detekciju klase 1
import csv
import subprocess
import os

print("Početak programa")

def pull_images_from_docker():
    # Pokreni Docker kontejner
    subprocess.run(["docker", "run", "--name", "virtual_competition", "ramimarinerobots/virtual-competition-2023"], check=True)

    # Kopiraj slike iz kontejnera
    subprocess.run(["docker", "cp", "virtual_competition:/data/images", "./local_images"], check=True)

    # Provjeri jesu li slike preuzete
    if not os.path.exists("./local_images"):
        raise FileNotFoundError("Slike nisu pronađene!")
    print("Slike uspješno preuzete.")

# Pokreni funkciju prije pipeline-a
pull_images_from_docker()

def merge_pipeline(image_path, txt_data, output_csv, ocr_model_dir):
    """
    Glavni pipeline koji integrira Lovrin, Bartulov i Lucijin dio.
    """
    try:
        # 1. Detekcija objekata (Lovrin model)
        detection_results = process_image(image_path)

        # 2. OCR prepoznavanje (Bartulov model s lokalnim direktorijem)
        ocr_results = process_ocr(image_path, model_dir=ocr_model_dir)

        # 3. Analiza boja za klasu 1 (Lucijin dio)
        # Samo ako postoji klasa 1 među detekcijama
        class1_color = None
        for det in detection_results:
            if det["class"] == 1:
                class1_color = color(image_path, klasa=1)
                break

        # Spajanje podataka prema klasi
        final_results = []
        for det in detection_results:
            result_entry = {
                "timestamp": det["timestamp"],  # Vrijeme obrade
                "class": det["class"],  # Klasa objekta
                "instance": class1_color if det["class"] == 1 else "N/A",  # Samo za klasu 1
                "centroid_x": det["cx"],
                "centroid_y": det["cy"],
            }
            final_results.append(result_entry)

        # Generiranje CSV-a
        with open(output_csv, 'w', newline='') as f:
            fieldnames = ["timestamp", "class", "instance", "centroid_x", "centroid_y"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_results)

        print(f"Pipeline completed. Output saved to {output_csv}")

    except Exception as e:
        print(f"Greška u pipeline-u: {e}")

if __name__ == "__main__":
    print("Ulazak u main blok")
    # Putanje do ulaznih podataka
    image_path = "local_images/sample_image.jpg"  # Pretpostavljam da Docker povuče slike ovdje
    ocr_model_dir = "OCR/inference OCR model"  # Prilagoditi putanju
    output_csv = "final_output.csv"

    # Poziv funkcije merge_pipeline
    merge_pipeline(
        image_path=image_path,
        txt_data=None,  # Pretpostavljam da txt_data nije potreban jer se oslanja na proces_image
        ocr_model_dir=ocr_model_dir,
        output_csv=output_csv
    )
