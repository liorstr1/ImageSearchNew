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
    all_image_files = get_image_files_from_folder(r"C:\Users\liors\Desktop\ocr", full_path=True)
    for img in all_image_files:
        json_path = os.path.splitext(img)[0] + ".json"
        if os.path.exists(json_path):
            continue
        analyze_image = AnalyzeImage(img, need_url=True)
        analyze_image.get_description_for_one_image('heb')


if __name__ == '__main__':
    # ocr_process()
    main_process()
