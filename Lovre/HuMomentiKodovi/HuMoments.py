import cv2
import numpy as np
import os


def calculate_hu_moments(image_path):
    """
    Izračun Hu-momenata za konturu u slici.
    """
    # Učitavanje slike i pretvaranje u grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Binarizacija slike
    _, binary = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)

    # Pronalaženje kontura
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Provjera ako nema kontura
    if not contours:
        print(f"Nema kontura u slici: {image_path}")
        return []

    hu_moments_list = []

    # Iteracija kroz sve konture
    for contour in contours:
        # Izračun geometrijskih momenata
        moments = cv2.moments(contour)

        # Izračun Hu-momenata
        hu_moments = cv2.HuMoments(moments).flatten()

        # Log-transformacija za normalizaciju vrijednosti
        hu_moments = -np.sign(hu_moments) * np.log10(np.abs(hu_moments) + 1e-8)

        hu_moments_list.append(hu_moments)

    return hu_moments_list


def calculate_reference_hu_values(image_paths):
    """
    Računa referentne Hu-momente kao prosjek za sve slike u jednoj klasi.
    """
    all_hu_moments = []
    for path in image_paths:
        hu_moments = calculate_hu_moments(path)
        if hu_moments:
            all_hu_moments.extend(hu_moments)  # Dodavanje svih Hu-momenata uzoraka

    if not all_hu_moments:
        raise ValueError("Nema valjanih Hu-momenata za zadane slike.")

    # Računanje prosječne vrijednosti za svaki Hu-moment
    reference_hu = np.mean(all_hu_moments, axis=0)
    return reference_hu


def classify_object(test_image_path, ring_pole_reference, cross_valve_reference):
    """
    Klasifikacija novog uzorka na temelju udaljenosti Hu-momenata.
    """
    test_hu = calculate_hu_moments(test_image_path)

    if not test_hu:
        return "Nije moguće klasificirati: nema kontura."

    test_hu = test_hu[0]  # Pretpostavljamo jednu dominantnu konturu

    # Izračunavanje Euklidske udaljenosti
    distance_ring_pole = np.linalg.norm(test_hu - ring_pole_reference)
    distance_cross_valve = np.linalg.norm(test_hu - cross_valve_reference)

    # Povratak klase s manjom udaljenošću
    if distance_ring_pole < distance_cross_valve:
        return "Ring Pole"
    else:
        return "Cross Valve"


# Glavni dio programa
if __name__ == "__main__":
    # Definirajte putanje do slika za svaku klasu
    ring_pole_images = ["path/to/ring1.jpg", "path/to/ring2.jpg", "path/to/ring3.jpg"]  # Zamijeniti stvarnim putanjama
    cross_valve_images = ["path/to/cross1.jpg", "path/to/cross2.jpg", "path/to/cross3.jpg"]

    try:
        # Računanje referentnih vrijednosti
        ring_pole_reference = calculate_reference_hu_values(ring_pole_images)
        cross_valve_reference = calculate_reference_hu_values(cross_valve_images)

        print("Referentni Hu-momenti za Ring Pole:", ring_pole_reference)
        print("Referentni Hu-momenti za Cross Valve:", cross_valve_reference)

        # Testiranje s novim uzorkom
        test_image_path = "path/to/test_image.jpg"  # Zamijeniti stvarnom putanjom
        result = classify_object(test_image_path, ring_pole_reference, cross_valve_reference)
        print(f"Klasifikacija za {test_image_path}: {result}")

    except Exception as e:
        print(f"Dogodila se pogreška: {e}")
