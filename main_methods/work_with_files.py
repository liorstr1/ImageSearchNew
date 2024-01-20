import os


def get_image_files_from_folder(folder_path, full_path=False):
    all_files = os.listdir(folder_path)
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    image_files = []
    for f in all_files:
        file_path = os.path.join(folder_path, f)
        extension = os.path.splitext(file_path)[1]
        if extension in image_extensions:
            if full_path:
                image_files.append(file_path)
            else:
                image_files.append(f)
    return image_files
