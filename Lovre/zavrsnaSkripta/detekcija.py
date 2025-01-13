from ultralytics import YOLO
import time

# Učitavanje YOLO modela iz .pt datoteke
model_path = "cropNovi.pt"  # Putanja do vašeg modela
model = YOLO(model_path)

# Funkcija za obradu slike
def process_image(image):
    # Provjera je li slika ispravno učitana
    if image is None:
        print("Greška: Slika nije učitana!")
        return []

    # Detekcija objekata pomoću YOLO modela
    results = model.predict(source=image, conf=0.5, save=False)  # confidence threshold = 0.5
    detections = results[0].boxes  # Bounding boxes

    output_data = []  # Lista za spremanje rezultata

    # Iteracija kroz sve detekcije
    for detection in detections:
        # Dobivanje bounding box-a i klase
        x1, y1, x2, y2 = map(int, detection.xyxy[0])  # Koordinate (x1, y1, x2, y2)
        class_id = int(detection.cls[0])  # ID klase
        class_name = model.names[class_id]  # Naziv klase

        # Centroid
        cx = detection.xywh[0][0]  # x centroid
        cy = detection.xywh[0][1]  # y centroid

        # Izrezivanje (crop) detektiranog objekta
        cropped_image = image[y1:y2, x1:x2]
        timestamp = int(time.time())
        # Spremanje rezultata u listu
        output_data.append({
            "class": class_id,
            "cx": cx,
            "cy": cy,
            "timestamp": timestamp,
            "crop": cropped_image
        })

    return output_data
