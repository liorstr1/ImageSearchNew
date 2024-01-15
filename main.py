import os

from main_methods.analyze_image import AnalyzeImage
from main_methods.work_with_files import get_image_files_from_folder


def main_process():
    all_images = get_image_files_from_folder('./images')
    test_image = all_images[1]
    analyze_image = AnalyzeImage(test_image, need_url=True)
    analyze_image.analyze_image_using_replicate()

    h = 0


def ocr_process():
    ocr_path = "C:/Users/liors/Desktop/ocr/ocr1.jpg"
    analyze_image = AnalyzeImage(ocr_path, need_url=True)
    analyze_image.get_ocr_from_image('heb')


if __name__ == '__main__':
    ocr_process()
    main_process()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
