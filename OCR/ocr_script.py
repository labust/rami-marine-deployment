from paddleocr import PaddleOCR
from numpy import asarray

def process_ocr(cropped_image, model_dir):
    ocr = PaddleOCR(lang='en', rec_model_dir=model_dir, show_log = False)
    arr_image = asarray(cropped_image)

    ocr_results = ocr.ocr(arr_image, det=False, cls=False)

    for res in ocr_results:
        for line in res:
            return line[0]

    return ""
