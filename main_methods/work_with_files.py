import os


def get_image_files_from_folder(folder_path):
    all_files = os.listdir(folder_path)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    image_files = []
    for f in all_files:
        file_path = os.path.join(folder_path, f)
        extension = os.path.splitext(file_path)[1]
        if extension in image_extensions:
            image_files.append(f)
    return image_files
