import cv2
import os

def global_thresholding(input_dir, output_dir, threshold_value=128):
    os.makedirs(output_dir, exist_ok=True)  

    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  

            if image is not None:
                
                _, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)

                
                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, binary_image)
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Failed to load image: {img_path}")


input_dir = 'path'  
output_dir = 'path'  

global_thresholding(input_dir, output_dir, threshold_value=128)


print("All images processed sequentially and saved.")
