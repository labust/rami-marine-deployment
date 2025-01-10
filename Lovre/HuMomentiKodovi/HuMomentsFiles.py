import cv2
import numpy as np
import os
import csv

def calculate_hu_moments(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    moments = cv2.moments(binary)
    hu_moments = cv2.HuMoments(moments).flatten()
    return hu_moments

def calculate_class_reference(path_to_class_images):
    hu_moments_list = []
    for filename in os.listdir(path_to_class_images):
        image_path = os.path.join(path_to_class_images, filename)
        hu_moments = calculate_hu_moments(image_path)
        hu_moments_list.append(hu_moments)
    reference_values = np.mean(hu_moments_list, axis=0)
    return reference_values

# Paths to class images
ring_pole_path = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\HuMomentiKodovi\CrossValve'
cross_valve_path = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\HuMomentiKodovi\RingPole'

# Calculate reference values
ring_pole_reference = calculate_class_reference(ring_pole_path)
cross_valve_reference = calculate_class_reference(cross_valve_path)

# Save to CSV
with open('reference_hu_moments.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hu1', 'Hu2', 'Hu3', 'Hu4', 'Hu5', 'Hu6', 'Hu7', 'Class'])
    writer.writerow([*ring_pole_reference, 'Ring Pole'])
    writer.writerow([*cross_valve_reference, 'Cross Valve'])

print("Referentne vrijednosti spremljene u 'reference_hu_moments.csv'")
