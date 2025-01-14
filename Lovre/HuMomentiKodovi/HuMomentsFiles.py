import cv2
import numpy as np
import os
import csv

# Funkcija za kreiranje maske i izračunavanje Hu-momenata
def calculate_hu_moments_with_masks(image_path):
    image = cv2.imread(image_path)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Definicije granica za boje
    lower_orange = np.array([10, 100, 150])  # Stroge granice za narandžastu
    upper_orange = np.array([25, 255, 255])

    lower_red1 = np.array([0, 120, 150])  # Stroge granice za crvenu (prvi opseg)
    upper_red1 = np.array([5, 255, 255])

    lower_red2 = np.array([170, 120, 150])  # Stroge granice za crvenu (drugi opseg)
    upper_red2 = np.array([180, 255, 255])

    # Kreiranje maski
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    red_mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Kombinovanje maski i izbor dominantne boje
    orange_pixels = cv2.countNonZero(orange_mask)
    red_pixels = cv2.countNonZero(red_mask)

    if orange_pixels > red_pixels and orange_pixels > 0:
        mask = orange_mask
    elif red_pixels > 0:
        mask = red_mask
    else:
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Izračunavanje Hu-momenata iz maske
    moments = cv2.moments(mask)
    hu_moments = cv2.HuMoments(moments).flatten()
    return hu_moments

# Funkcija za računanje referentnih vrednosti za klasu
def calculate_class_reference(path_to_class_images):
    hu_moments_list = []
    for filename in os.listdir(path_to_class_images):
        image_path = os.path.join(path_to_class_images, filename)
        hu_moments = calculate_hu_moments_with_masks(image_path)
        hu_moments_list.append(hu_moments)
    reference_values = np.mean(hu_moments_list, axis=0)
    return reference_values

# Putanje do slika klasa
ring_pole_path = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\HuMomentiKodovi\CrossValve'
cross_valve_path = r'C:\Users\Lovre\PROJEKT-R\yolo11-test\HuMomentiKodovi\RingPole'

# Računanje referentnih vrednosti
ring_pole_reference = calculate_class_reference(ring_pole_path)
cross_valve_reference = calculate_class_reference(cross_valve_path)

# Snimanje u CSV
with open('reference_hu_moments.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Hu1', 'Hu2', 'Hu3', 'Hu4', 'Hu5', 'Hu6', 'Hu7', 'Class'])
    writer.writerow([*ring_pole_reference, 'Ring Pole'])
    writer.writerow([*cross_valve_reference, 'Cross Valve'])

print("Referentne vrijednosti spremljene u 'reference_hu_moments.csv'")
