from Lovre.zavrsnaSkripta.detekcija import process_image
from OCR.ocr_script import process_ocr
from Lucija.cr import color  # Funkcija za detekciju klase 1
import csv
import subprocess
import os
import cv2
import sys

print("Početak programa")
def classify_object(width, height):
    """
    Klasificira bounding box na temelju omjera visina/širina.
    """
    aspect_ratio = height / width
    if aspect_ratio > 1.5 or aspect_ratio < 0.75:  # Prilagodi prag za ring pole
        return "Ring Pole"
    else:
        return "Cross-shaped Valve"

def pull_images_from_docker():
    # Pokreni Docker kontejner
    subprocess.run(["docker", "run", "--name", "virtual_competition", "ramimarinerobots/virtual-competition-2023"], check=True)

    # Kopiraj slike iz kontejnera
    subprocess.run(["docker", "cp", "virtual_competition:/home/rami/rami_marine_dataset", "./local_images"], check=True)

    # Provjeri jesu li slike preuzete
    if not os.path.exists("./local_images"):
        raise FileNotFoundError("Slike nisu pronađene!")
    print("Slike uspješno preuzete.")

# Pokreni funkciju prije pipeline-a
#pull_images_from_docker()

def merge_pipeline(image_path, txt_data, output_csv, ocr_model_dir):
    """
    Glavni pipeline koji integrira Lovrin, Bartulov i Lucijin dio.
    """
    print("haha")
    try:
        # 1. Detekcija objekata (Lovrin model)
        try:
            image = cv2.imread(image_path)
            print(f"Pokrećem process_image za: {image_path}")
            detection_results = process_image(image)
            print("Rezultat detekcije objekata:", detection_results)
        except Exception as e:
            print(f"Greška u process_image: {e}")
            raise  # Ponovno podiže grešku nakon ispisa


        # 2. OCR prepoznavanje (Bartulov model s lokalnim direktorijem)
        print("pocinjem s ocr")
        

        
        instance = None
        for det in detection_results:
            if (det["class"]+1 == 2  or det["class"]+1 == 3 ):
                instance = process_ocr(image, model_dir=ocr_model_dir)
                break
        # 3. Analiza boja za klasu 1 (Lucijin dio)
        # Samo ako postoji klasa 1 među detekcijama
        
        for det in detection_results:
            if det["class"]+1 == 1:
                instance = color(image, klasa=1)
                break
        height, width, channels = image.shape
        for det in detection_results:
            if det["class"]+1 == 5:
                instance = classify_object(width, height)
                break

        # Spajanje podataka prema klasi
        final_results = []
        for det in detection_results:
            result_entry = {
                "timestamp": det["timestamp"],  # Vrijeme obrade
                "class": det["class"]+1,  # Klasa objekta
                "instance": instance,  # Samo za klasu 1
                "centroid_x": det["cx"],
                "centroid_y": det["cy"],
            }
            final_results.append(result_entry)

        # Generiranje CSV-a
        with open(output_csv, 'a', newline='') as f:
            fieldnames = ["timestamp", "class", "instance", "centroid_x", "centroid_y"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_results)

        print(f"Pipeline completed. Output saved to {output_csv}")

    except Exception as e:
        print(f"Greška u pipeline-u: {e}")

if __name__ == "__main__":
    print("Ulazak u main blok")
    input_image_path = sys.argv[1]
    print(input_image_path)
    # Putanje do ulaznih podataka
    image_path = input_image_path  # Pretpostavljam da Docker povuče slike ovdje
    ocr_model_dir = "OCR/inference OCR model v4"  # Prilagoditi putanju
    output_csv = sys.argv[2]
    #image_paths=["local_images/class_1/yellow/img_0006.png",
     #            "local_images/class_2/number_2/img_0025.png",
      #           "local_images/class_3/number_6/img_0012.png",
       #          "local_images/class_4/img_0006.png",
        #         "local_images/class_5/img_012.jpg",
         #        "local_images/class_6/img_0006.jpg"]
    # Poziv funkcije merge_pipeline
    #for image_path in image_paths:
    #    merge_pipeline(
    #        image_path=image_path,
    #        txt_data=None,  # Pretpostavljam da txt_data nije potreban jer se oslanja na proces_image
    #        ocr_model_dir=ocr_model_dir,
    #        output_csv=output_csv
    #    )
    merge_pipeline(
            image_path=image_path,
            txt_data=None,  # Pretpostavljam da txt_data nije potreban jer se oslanja na proces_image
            ocr_model_dir=ocr_model_dir,
            output_csv=output_csv
        )
