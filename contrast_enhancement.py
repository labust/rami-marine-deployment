import cv2
import os
import numpy as np

def histogram_equalization(image):
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    yuv_image[:, :, 0] = cv2.equalizeHist(yuv_image[:, :, 0])
    return cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)

def clahe_contrast_enhancement(image):
    yuv_image = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    yuv_image[:, :, 0] = clahe.apply(yuv_image[:, :, 0])
    return cv2.cvtColor(yuv_image, cv2.COLOR_YUV2BGR)

def gamma_correction(image, gamma=1.2):
    normalized = image / 255.0
    corrected = np.power(normalized, gamma)
    return np.uint8(corrected * 255)


input_dir = 'path'  
output_dir = 'path' 


os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    
    if filename.endswith(('.jpg', '.jpeg', '.png')):
       
        img_path = os.path.join(input_dir, filename)

        
        image = cv2.imread(img_path)

        if image is not None:
            enhanced_image = clahe_contrast_enhancement(image) 
            enhanced_image = histogram_equalization(enhanced_image) 
            enhanced_image = gamma_correction(enhanced_image, gamma=1.2)

            
            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, enhanced_image)

            print(f"Processed and saved: {output_path}")
        else:
            print(f"Failed to load image: {img_path}")

print("All images processed sequentially and saved with original filenames.")

