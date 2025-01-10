import os
import csv
from paddleocr import PaddleOCR
from datetime import datetime

ocr = PaddleOCR(lang='en', rec_model_dir="C:/Users/Makedonski ajvar/PaddleOCR/tools/output/test1/inference OCR model v2")

txt_file_path = "C:/Users/Makedonski ajvar/Downloads/images/input.txt"
csv_file_path = "C:/Users/Makedonski ajvar/Downloads/images/youroutput.csv"
image_path = "C:/Users/Makedonski ajvar/PaddleOCR/train_data/rec/train/3_0082_crop_0_ce.jpg"

with open(txt_file_path, 'r') as f:
    txt_data = f.readlines()

with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    
    if os.path.exists(image_path):
        print(f"Processing {os.path.basename(image_path)}")

        result = ocr.ocr(image_path, det=False, cls=False)

        for idx in range(len(result)):
            ocr_data = result[idx]
            for line in ocr_data:
                class_id, x_center, y_center, width, height = map(float, txt_data[idx].split())

                ocr_result = line[0] 
                timestamp = int(datetime.timestamp(datetime.now()))
                writer.writerow([timestamp, int(class_id), ocr_result, x_center, y_center])

        print(f"CSV file saved at {csv_file_path}")
    else:
        print(f"The specified image does not exist: {image_path}")
