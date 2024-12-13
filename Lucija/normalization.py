import cv2
import numpy as np
import os

def min_max_normalization(image):

    image_float = image.astype(np.float32)

    normalized_image = (image_float - np.min(image_float)) / (np.max(image_float) - np.min(image_float))
    return normalized_image

input_dir = 'path'  
output_dir = 'path'  

os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        
        img_path = os.path.join(input_dir, filename)

        
        image = cv2.imread(img_path)

        if image is not None:
            
            normalized_image = min_max_normalization(image)

            
            normalized_image_uint8 = (normalized_image * 255).astype(np.uint8)

            
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, normalized_image_uint8)

            print(f"Normalized and saved: {output_path}")
        else:
            print(f"Failed to load image: {img_path}")

print("All images processed sequentially and saved.")
