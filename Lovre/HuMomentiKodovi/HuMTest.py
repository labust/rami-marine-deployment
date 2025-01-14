import cv2
import numpy as np
import csv


# Funkcija za učitavanje referentnih vrednosti iz CSV datoteke
def load_reference_values(csv_path):
    references = {}
    with open(csv_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            class_name = row['Class']
            hu_values = [float(row[f'Hu{i + 1}']) for i in range(7)]
            references[class_name] = np.array(hu_values)
    return references


# Funkcija za izračun Hu-momenata iz maske
def calculate_hu_moments_from_mask(mask):
    moments = cv2.moments(mask)
    return cv2.HuMoments(moments).flatten()


# Funkcija za testiranje slike na dominantnu boju i primenu odgovarajuće obrade
def test_and_process_image(image_path, reference_values):
    # Učitavanje slike u boji
    image = cv2.imread(image_path)

    # Pretvaranje slike u HSV format
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Granice za narandžastu boju (HSV vrednosti)
    # Postrožene granice za narandžastu boju
    lower_orange = np.array([10, 100, 150])  # Strože granice za narandžastu
    upper_orange = np.array([25, 255, 255])

    # Postrožene granice za crvenu boju
    lower_red1 = np.array([0, 120, 150])  # Strože granice za crvenu
    upper_red1 = np.array([5, 255, 255])

    lower_red2 = np.array([170, 120, 150])  # Sekundarni stroži opseg za crvenu
    upper_red2 = np.array([180, 255, 255])

    # Kreiranje maski za narandžastu i crvenu boju
    orange_mask = cv2.inRange(hsv_image, lower_orange, upper_orange)
    red_mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    red_mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)  # Kombinacija crvenih opsega

    # Brojanje piksela za svaku masku
    orange_pixels = cv2.countNonZero(orange_mask)
    red_pixels = cv2.countNonZero(red_mask)

    # Odabir maske na osnovu dominacije boje
    if orange_pixels > red_pixels and orange_pixels > 0:
        mask = orange_mask
        print("Narandžasta boja dominira.")
    elif red_pixels > 0:
        mask = red_mask
        print("Crvena boja dominira.")
    else:
        print("Nema dominantne boje. Koristi se grayscale.")
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        mask = gray_image

    # Računanje Hu-momenata za odabranu masku
    hu_moments = calculate_hu_moments_from_mask(mask)

    # Poređenje Hu-momenata sa referentnim vrednostima
    min_distance = float('inf')
    closest_class = None
    for class_name, reference_hu in reference_values.items():
        distance = np.linalg.norm(hu_moments - reference_hu)
        if distance < min_distance:
            min_distance = distance
            closest_class = class_name

    print(f"Predviđena klasa: {closest_class}")
    print(f"Euclidovska udaljenost: {min_distance}")

    return image, mask, closest_class


# Putanja do testne slike
test_image_path = 'testovi/test10.jpg'  # Zamenite sa stvarnom putanjom do slike
reference_csv_path = 'reference_hu_moments2.csv'
reference_values = load_reference_values(reference_csv_path)

# Testiranje slike i primena obrade
processed_image, mask, predicted_class = test_and_process_image(test_image_path, reference_values)

# Prikaz rezultata
if mask is not None:
    cv2.imshow("Maska", mask)

cv2.imshow("Processed Image", processed_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
