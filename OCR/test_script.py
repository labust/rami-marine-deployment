import os
from paddleocr import PaddleOCR
ocr = PaddleOCR(lang='en', rec_model_dir="C:/Users/Makedonski ajvar/PaddleOCR/tools/output/test7/best") # need to run only once to load model into memory
dir_path = r"C:\Users\Makedonski ajvar\Downloads\images"

for img_name in os.listdir(dir_path):
    img_path = dir_path + '\\' + img_name
    print(img_name)
    result = ocr.ocr(img_path, det=False, cls=False)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)
