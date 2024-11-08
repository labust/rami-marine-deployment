import cv2
import os

def grayscale_images(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)  

    for filename in os.listdir(input_dir):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            img_path = os.path.join(input_dir, filename)
            image = cv2.imread(img_path)

            if image is not None:
                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


                output_path = os.path.join(output_dir, filename)
                cv2.imwrite(output_path, gray_image)
                print(f"Processed and saved: {output_path}")
            else:
                print(f"Failed to load image: {img_path}")

input_dir = 'path'  
output_dir = 'path'   


grayscale_images(input_dir, output_dir)
print("All images processed sequentially and saved.")
