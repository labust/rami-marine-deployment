import cv2
from detekcija import process_image  # Import funkcije iz prve skripte

# Učitavanje slike (kao podatka)
image = cv2.imread("testnaSlika.jpg")  # Zamijenite sa svojom metodom za dohvat slike

# Procesiraj sliku
detections = process_image(image)

# Obrada rezultata
for i, detection in enumerate(detections):
    print(f"Objekt {i + 1}:")
    print(f" - Klasa: {detection['class']}")
    print(f" - Centroid cx: {detection['cx']} i cy: {detection['cy']}")
    print(f" - timestamp {detection['timestamp']}:")
    # Prikaz cropane slike
    cv2.imshow(f"Crop {i + 1}", detection["crop"])

cv2.waitKey(0)
cv2.destroyAllWindows()
