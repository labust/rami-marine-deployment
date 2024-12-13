import cv2
import os

def adaptive_thresholding(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)  

    
    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  

            if image is not None:
                
                binary_image = cv2.adaptiveThreshold(image, 255,
                                                     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                     cv2.THRESH_BINARY,
                                                     11, 2)  

                
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, binary_image)
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Failed to load image: {img_path}")


input_dir = 'path'  
output_dir = 'path' 


adaptive_thresholding(input_dir, output_dir)
print("All images processed sequentially and saved.")
