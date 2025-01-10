import cv2
import numpy as np
import csv
import os

# Funkcija za učitavanje referentnih vrijednosti iz CSV datoteke
def load_reference_values(csv_path):
    references = {}
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            class_name = row['Class']
            hu_values = [float(row[f'Hu{i+1}']) for i in range(7)]
            references[class_name] = np.array(hu_values)
    return references

# Funkcija za izračun Hu-momenata za novu sliku
def calculate_hu_moments(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    moments = cv2.moments(binary)
    hu_moments = cv2.HuMoments(moments).flatten()
    return hu_moments

# Funkcija za testiranje Hu-momenata nove slike
def test_image(image_path, reference_values):
    hu_moments = calculate_hu_moments(image_path)
    min_distance = float('inf')
    closest_class = None
    for class_name, reference_hu in reference_values.items():
        distance = np.linalg.norm(hu_moments - reference_hu)
        if distance < min_distance:
            min_distance = distance
            closest_class = class_name
    return closest_class, min_distance

# Putanja do testne slike
test_image_path = 'testovi/test7.jpg'


reference_csv_path = 'reference_hu_moments.csv'
reference_values = load_reference_values(reference_csv_path)

# Testiranje slike
predicted_class, distance = test_image(test_image_path, reference_values)
print(f"Predviđena klasa: {predicted_class}")
print(f"Euclidovska udaljenost: {distance}")
