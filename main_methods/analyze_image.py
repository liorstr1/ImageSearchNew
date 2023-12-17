import os
from imgurpython import ImgurClient

from main_methods.connect_to_models import (
    get_description_from_cogvlm, get_list_of_objects_from_gpt4, get_coordinates_from_llava, get_description_from_llava
)
from main_methods.helper_methods import (
    try_get_description, save_full_description, try_get_data_from_json, save_data_to_json
)
from main_methods.work_with_imgur import convert_file_to_url, delete_url_image
from prompts import get_data_from_image_prompts
from dotenv import load_dotenv

load_dotenv()
IMGUR_CLIENT_ID = os.getenv('IMGUR_CLIENT_ID')
IMGUR_CLIENT_SECRET = os.getenv('IMGUR_CLIENT_SECRET')


class AnalyzeImage:
    # Define a class 'AnalyzeImage' for image analysis.

    def __init__(self, image_name, need_url=False):
        # Constructor to initialize an AnalyzeImage object.
        # 'image_path' specifies the location of the image to be analyzed.
        # 'need_url' is a flag to determine if an Imgur URL is needed for the image.

        self.need_url = need_url
        self.image_path = os.path.join(os.getenv('IMAGES_FOLDER'), image_name)
        # Store the provided image path.
        self.description_path = os.path.join(os.getenv('DESCRIPTION_FOLDER'), os.path.splitext(image_name)[0] + '.txt')
        self.objects_list_path = os.path.join(
            os.getenv('OBJECTS_LIST_FOLDER'), os.path.splitext(image_name)[0] + '_obj.txt'
        )
        self.objects2coord_path = os.path.join(
            os.getenv('OBJECTS_COORDS_FOLDER'), os.path.splitext(image_name)[0] + '_coords.json'
        )
        self.objects2description_path = os.path.join(
            os.getenv('OBJECTS_DESCRIPTIONS_FOLDER'), os.path.splitext(image_name)[0] + '_descriptions.json'
        )
        self.replicate_api = os.getenv('REPLICATE_API_TOKEN')
        # Retrieve Replicate API key from environment variables.

        self.image_url = None
        self.image_deletehash = None
        # Store the 'need_url' flag.

        if self.need_url:
            # Check if an Imgur URL is required.

            self.imgur_client = ImgurClient(IMGUR_CLIENT_ID, IMGUR_CLIENT_SECRET)
            # Initialize an ImgurClient with the provided credentials.

            self.image_url, self.image_deletehash = convert_file_to_url(
                self.image_path,
                self.imgur_client
            )
            # Convert the image file to an Imgur URL and store the URL and deletehash.

    def __del__(self):
        # Destructor to clean up when an instance of AnalyzeImage is deleted.

        if self.need_url:
            # Check if an Imgur URL was created.
            try:
                delete_url_image(self.image_deletehash, self.imgur_client)
            except Exception as e:
                print("image didn't delete from imgur")
            # Delete the image from Imgur using the stored deletehash.

    def analyze_image_using_replicate(self):
        # get first the full description
        full_description = self.get_full_description()
        # get list of objects
        list_of_objects = self.get_list_of_objects(full_description)
        object2coordinates = self.get_coordinates_of_objects(list_of_objects)
        object2description = self.get_description_for_all_objects(object2coordinates)
        h = 0

    def get_full_description(self):
        full_description = try_get_description(self.description_path)
        if full_description is None:
            full_description = get_description_from_cogvlm(
                self.image_url,
                get_data_from_image_prompts.GET_FULL_DESCRIPTION,
            )
            if full_description is None:
                raise Exception("full_description is None. Terminating the program.")

            save_full_description(self.description_path, full_description)
        return full_description

    def get_list_of_objects(self, full_description):
        list_of_objects = try_get_data_from_json(self.objects_list_path)
        if list_of_objects is None:
            list_of_objects = get_list_of_objects_from_gpt4(full_description)
            if list_of_objects is None:
                raise Exception("list_of_objects is None. Terminating the program.")
            save_data_to_json(self.objects_list_path, list_of_objects)
        return list_of_objects

    def get_coordinates_of_objects(self, list_of_objects):
        object2coordinates = try_get_data_from_json(self.objects2coord_path)
        if object2coordinates is None:
            object2coordinates = get_coordinates_from_llava(self.image_url, list_of_objects)
            if object2coordinates is None:
                raise Exception("object2coordinates is None. Terminating the program.")
            save_data_to_json(self.objects2coord_path, object2coordinates)
        return object2coordinates

    def get_description_for_all_objects(self, object2coordinates):
        object2description = try_get_data_from_json(self.objects2description_path)
        if object2description is None:
            object2description = {}
            for c, coords in object2coordinates.items():
                object2description[c] = get_description_from_llava(self.image_url, c, coords)
        pass









