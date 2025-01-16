from ultralytics import YOLO
#imena klasa su cross-valve i ringpole
# Učitavanje YOLO modela
model_path = "class5.pt"  # Putanja do vašeg modela
model = YOLO(model_path)

def class5_detection(image):

    # Provjera je li slika ispravno učitana
    if image is None:
        print("Greška: Slika nije učitana!")
        return None

    # Detekcija objekata pomoću YOLO modela
    results = model.predict(source=image, conf=0.5, save=False)  # confidence threshold = 0.5
    detections = results[0].boxes  # Bounding boxes

    # Provjera postoji li barem jedna detekcija
    if len(detections) == 0:
        print("Nema detektiranih objekata na slici.")
        return None

    # Pronalazak klase s najvećom vjerovatnošću
    best_detection = max(detections, key=lambda det: det.conf[0])  # Najveća vjerovatnoća
    class_id = int(best_detection.cls[0])  # ID klase
    class_name = model.names[class_id]  # Naziv klase

    return class_name
