import cv2
import os

input_dir = 'path'  
output_dir = 'path'  


os.makedirs(output_dir, exist_ok=True)


for filename in os.listdir(input_dir):
    
    if filename.endswith(('.jpg', '.jpeg', '.png')):
       
        img_path = os.path.join(input_dir, filename)

       
        image = cv2.imread(img_path)

        if image is not None:
            
            gaussian_blur = cv2.GaussianBlur(image, (5, 5), 0)

            
            median_blur = cv2.medianBlur(gaussian_blur, 5)

            
            final_processed_image = cv2.bilateralFilter(median_blur, 5, 75, 75)

            output_path = os.path.join(output_dir, filename)
            cv2.imwrite(output_path, final_processed_image)

            print(f"Processed and saved: {output_path}")
        else:
            print(f"Failed to load image: {img_path}")

print("All images processed sequentially and saved with original filenames.")

