import os
from paddleocr import PaddleOCR

def process_ocr(cropped_image, model_dir):
    ocr = PaddleOCR(lang='en', rec_model_dir=model_dir, show_log = False)

    ocr_results = ocr.ocr(cropped_image, det=False, cls=False)

    for res in ocr_results:
        for line in res:
            return line[0]

    return ""
