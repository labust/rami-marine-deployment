import os
import cv2
from Class5Det import class5_detection

# Putanja do direktorija sa slikama
images_folder = os.path.abspath(r"C:\Users\Lovre\PROJEKT-R\yolo11-test\HuMomentiKodovi\Testovi\Testovi4")  # Zamijenite s pravom putanjom

# Provjera postoji li direktorij
if not os.path.exists(images_folder):
    print(f"Greška: Direktorij {images_folder} ne postoji!")
    exit()

# Iteracija kroz sve slike u direktoriju
for image_name in os.listdir(images_folder):
    image_path = os.path.join(images_folder, image_name)

    # Provjera je li datoteka slika
    if not image_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        print(f"Preskačem: {image_name} nije podržana slika.")
        continue

    # Učitavanje slike
    try:
        image = cv2.imread(image_path)
    except Exception as e:
        print(f"Greška pri učitavanju slike {image_name}: {e}")
        continue

    # Provjera je li slika učitana
    if image is None:
        print(f"Greška: Slika {image_name} nije učitana ili nije podržana!")
        continue

    # Pozivanje funkcije za obradu slike
    detected_class = class5_detection(image)

    # Ispis rezultata
    if detected_class:
        print(f"Slika: {image_name}, Detektirana klasa: {detected_class}")
    else:
        print(f"Slika: {image_name}, Nema detekcija.")
