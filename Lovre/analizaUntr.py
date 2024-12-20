import os
import cv2
import numpy as np


def yolo_to_bbox(yolo_data, img_width, img_height):

    x_center, y_center, width, height = yolo_data
    x1 = int((x_center - width / 2) * img_width)
    y1 = int((y_center - height / 2) * img_height)
    x2 = int((x_center + width / 2) * img_width)
    y2 = int((y_center + height / 2) * img_height)
    return x1, y1, x2, y2


def analyze_shape(image):
    """Analizira oblik unutar bounding boxa i vraća 'Cross-Shaped Valve' ili 'Ring Pole'."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        area = cv2.contourArea(contour)
        if area > 100:  # Filtriraj male konture
            if len(approx) > 8:  # Kružno - Ring Pole
                return "Ring Pole"
            elif len(approx) <= 8:  # Linije - Cross-Shaped Valve
                return "Cross-Shaped Valve"
    return "Unknown"


def process_images(image_folder, label_folder, output_folder):
    """Procesira slike i prepoznaje objekte unutar bounding boxova."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_file in os.listdir(image_folder):
        if not image_file.endswith(('.jpg', '.png')):
            continue

        image_path = os.path.join(image_folder, image_file)
        label_path = os.path.join(label_folder, image_file.replace('.jpg', '.txt').replace('.png', '.txt'))

        if not os.path.exists(label_path):
            print(f"No label file for {image_file}. Skipping...")
            continue

        image = cv2.imread(image_path)
        img_height, img_width = image.shape[:2]

        # Čitaj oznake iz YOLO label datoteke
        with open(label_path, 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            parts = line.strip().split()
            yolo_data = list(map(float, parts[1:]))
            x1, y1, x2, y2 = yolo_to_bbox(yolo_data, img_width, img_height)
            cropped_img = image[y1:y2, x1:x2]

            # Analiziraj oblik unutar bounding boxa
            result = analyze_shape(cropped_img)
            print(f"Image: {image_file}, Box {i + 1}: {result}")

            # Spremi izrezani bounding box sa oznakom
            output_path = os.path.join(output_folder, f"{image_file}_box{i + 1}_{result}.jpg")
            cv2.imwrite(output_path, cropped_img)


# Postavi putanje
image_folder = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\test\images'  # Putanja do foldera sa slikama
label_folder = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\test\labels'  # Putanja do YOLO oznaka
output_folder = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\izlazUNTR'  # Putanja za spremanje rezultata

# Pokreni skriptu
process_images(image_folder, label_folder, output_folder)
