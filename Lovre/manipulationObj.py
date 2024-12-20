import os
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

def calculate_aspect_ratios(annotation_dir, image_dir):
    aspect_ratios = []

    for annotation_file in os.listdir(annotation_dir):
        if annotation_file.endswith('.txt'):

            image_file = os.path.splitext(annotation_file)[0] + ".jpg"
            image_path = os.path.join(image_dir, image_file)
            annotation_path = os.path.join(annotation_dir, annotation_file)

            if not os.path.exists(image_path):
                print(f"Slika {image_file} ne postoji! Preskačem...")
                continue


            with Image.open(image_path) as img:
                image_width, image_height = img.size


            with open(annotation_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 5:
                        _, _, _, bbox_width, bbox_height = map(float, parts)
                        # Denormalizacija bounding box dimenzija
                        bbox_width *= image_width
                        bbox_height *= image_height
                        # Računanje omjera
                        if bbox_height > 0:  # Izbjegavanje dijeljenja s nulom
                            aspect_ratio = bbox_width / bbox_height
                            aspect_ratios.append(aspect_ratio)
    return aspect_ratios



annotation_directory = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\test\labels'  # Putanja do YOLO anotacija
image_directory = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\klasa5.yolov11\test\images'  # Putanja do slika


ratios = calculate_aspect_ratios(annotation_directory, image_directory)


print(f"Broj bounding boxova: {len(ratios)}")
print(f"Prosječni omjer: {np.mean(ratios):.2f}")
print(f"Min omjer: {np.min(ratios):.2f}")
print(f"Max omjer: {np.max(ratios):.2f}")



plt.hist(ratios, bins=20, color='skyblue', edgecolor='black')
plt.xlabel('Aspect Ratio (Width / Height)')
plt.ylabel('Frequency')
plt.title('Distribution of Bounding Box Aspect Ratios')
plt.show()
