import os
from imgurpython import ImgurClient

from main_methods.connect_to_models import (
    get_description_from_cogvlm, get_list_of_objects_from_gpt4, get_coordinates_from_llava, get_description_from_llava,
    get_struct_from_mistral
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
        self.json_struct_path = os.getenv('JSON_STRUCTS_FOLDER')
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
        type2json_structure = self.get_json_structure(
            list(set([d['type'] for o, d in object2coordinates.items()])),
        )
        object2description = self.get_description_for_all_objects(object2coordinates, type2json_structure)
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

    def get_list_of_objects(self, full_description, override=False):
        list_of_objects = try_get_data_from_json(self.objects_list_path)
        if list_of_objects is None or override:
            list_of_objects = get_list_of_objects_from_gpt4(full_description, model='gpt-3.5-turbo-1106')
            if list_of_objects is None:
                raise Exception("list_of_objects is None. Terminating the program.")
            save_data_to_json(self.objects_list_path, list_of_objects)
        return {o['object']: {'type': o['type_of_object']} for o in list_of_objects}

    def get_coordinates_of_objects(self, list_of_objects, override=False):
        def update_list_of_objects(ob, coordinates):
            list_of_objects[ob]['coords'] = coordinates

        object2coordinates = try_get_data_from_json(self.objects2coord_path)
        if object2coordinates is None or override:
            object2coordinates = get_coordinates_from_llava(self.image_url, list(list_of_objects.keys()))
            if object2coordinates is None:
                raise Exception("object2coordinates is None. Terminating the program.")
            save_data_to_json(self.objects2coord_path, object2coordinates)
        [update_list_of_objects(o, coords) for o, coords in object2coordinates.items()]
        return list_of_objects

    def get_description_for_all_objects(self, object2coordinates, type2json_structure):
        object2description = try_get_data_from_json(self.objects2description_path)
        if object2description is None:
            object2description = {}
            for obj, data in object2coordinates.items():
                object2description[obj] = get_description_from_llava(
                    self.image_url,
                    obj,
                    data['coords'],
                    type2json_structure[data['type']]
            )
            save_data_to_json(self.objects2description_path, object2description)
        return object2description

    def get_json_structure(self, list_of_types):
        res = {}
        for t in list_of_types:
            t_path = os.path.join(self.json_struct_path, f'{t}_object.json')
            t_struct = try_get_data_from_json(t_path)
            if t_struct is None:
                t_struct = get_struct_from_mistral(t)
                if t_struct is None:
                    raise Exception("t_struct is None. Terminating the program.")
                save_data_to_json(t_path, t_struct)
            res[t] = t_struct
        return res









