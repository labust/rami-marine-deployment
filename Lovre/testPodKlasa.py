import os
import cv2

# Funkcija za čitanje bounding boxa iz YOLO anotacija
def read_yolo_annotations(annotation_path):

    boxes = []
    with open(annotation_path, 'r') as file:
        for line in file:
            # Svaki redak: class x_center y_center width height (sve normalizirano 0-1)
            parts = line.strip().split()
            if len(parts) == 5:
                class_id = int(parts[0])  # Klasa (za sada sve == manipulation object)
                x_center, y_center, width, height = map(float, parts[1:])
                boxes.append((class_id, x_center, y_center, width, height))
    return boxes

# Funkcija za razlikovanje objekata prema aspect ratio
def classify_object(width, height):
    """
    Klasificira bounding box na temelju omjera visina/širina.
    """
    aspect_ratio = height / width
    if aspect_ratio > 1.5 or aspect_ratio < 0.75:  # Prilagodi prag za ring pole
        return "Ring Pole"
    else:
        return "Cross-shaped Valve"

# Glavna funkcija za procesiranje slika i anotacija
def process_images_and_annotations(image_folder, annotation_folder, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for annotation_file in os.listdir(annotation_folder):
        if annotation_file.endswith('.txt'):
            image_file = annotation_file.replace('.txt', '.jpg')  # Pretpostavka: .jpg slike
            image_path = os.path.join(image_folder, image_file)
            annotation_path = os.path.join(annotation_folder, annotation_file)

            if not os.path.exists(image_path):
                print(f"Slika nedostaje za anotaciju: {image_path}")
                continue

            # Učitavanje slike
            image = cv2.imread(image_path)
            height, width = image.shape[:2]

            # Čitanje bounding boxova
            boxes = read_yolo_annotations(annotation_path)

            for idx, (class_id, x_center, y_center, w, h) in enumerate(boxes):
                # Preračunavanje u piksele
                x_center_pixel = int(x_center * width)
                y_center_pixel = int(y_center * height)
                box_width = int(w * width)
                box_height = int(h * height)

                x1 = int(x_center_pixel - box_width / 2)
                y1 = int(y_center_pixel - box_height / 2)
                x2 = int(x_center_pixel + box_width / 2)
                y2 = int(y_center_pixel + box_height / 2)

                # Klasifikacija objekta
                object_type = classify_object(box_width, box_height)
                print(f"{image_file} - Objekt: {object_type}, Koordinate: ({x1}, {y1}), ({x2}, {y2})")

                # Izrezivanje bounding boxa i spremanje
                cropped_image = image[y1:y2, x1:x2]
                output_path = os.path.join(output_folder, f"{image_file}_{idx}_{object_type}.jpg")
                cv2.imwrite(output_path, cropped_image)

# Putanje
image_folder = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\test\images'  # Folder sa slikama
annotation_folder = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\test\labels'  # Folder sa YOLO anotacijama
output_folder = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\izlaz'  # Izlazni folder

process_images_and_annotations(image_folder, annotation_folder, output_folder)
