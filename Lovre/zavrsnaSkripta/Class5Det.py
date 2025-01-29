from ultralytics import YOLO


model_path = "class5.pt"
model = YOLO(model_path)


class_mapping = {
    "cross-valve": "x-shaped valve",
    "ringpole": "ring pole"
}

def class5_detection(image):
    # Provjera je li slika ispravno učitana
    if image is None:
        print("Greška: Slika nije učitana!")
        return None


    results = model.predict(source=image, conf=0.5, save=False)
    detections = results[0].boxes


    if len(detections) == 0:
        print("Nema detektiranih objekata na slici.")
        return None


    best_detection = max(detections, key=lambda det: det.conf[0])
    class_id = int(best_detection.cls[0])
    class_name = model.names[class_id]

    mapped_class_name = class_mapping.get(class_name, class_name)

    return mapped_class_name
