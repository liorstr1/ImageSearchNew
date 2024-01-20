GET_FULL_DESCRIPTION = """
    Please provide a comprehensive and detailed description of the following image. Focus on identifying and explaining
    all visible elements, including objects, people, their actions, and interactions. Describe the setting, including
    any background details, lighting, and atmosphere. Highlight any emotions or moods conveyed by the scene or the
    subjects within it. Also, mention the style and artistic elements if applicable, such as color palette, composition,
    and any notable textures or patterns. Offer insights into the possible context or story behind the image, including
    cultural or historical references if identifiable.
"""

LIST_OF_OBJECTS_PROMPT = """
Please analyze the text and identify the real-world objects that are mentioned in the text.
return the list in a JSON format: 
[
    {
        "object": the object in singular form e.g "boys" become "boy", "chairs" become "chair", 
        "object_type": the type of the object,
        "object_count": how many of these objects are mentioned in the text (if it's the same object mentioned twice count it as 1
    }...
] return just the json without any text before or after
"""

GET_COORDINATES_PROMPT = """
"for this list of objects: {list_of_objects} \n
create list of lists, each inner list contains the coordinates of one object
[
    {{
        "object_idx": the index of the object in the list,
        "object_name": the name of the object,
        "object_coordinates": the coordinates of the object in te image
    }}...
[
"""

GET_DESCRIPTION_PROMPT = """
in the next image {image}, in the following coordinates: {coords}, there is a {object},
fill the next JSON for this object:
{json_struct}
"""

GET_COORDINATES_FROM_TEXT_PROMPT = """
fix this text to be valid JSON format:
[
    {{
        "object_name": the name of the object,
        "object_coordinates": [the coordinates of the object in te image]
    }}...
[
"""

TYPE_STRUCT_PROMPT = """
I have an image featuring a {object_type} that I wish to describe in detail. Could you please provide me with a
comprehensive list of attributes to describe every aspect of the boy? I am seeking attributes that encompass his
physical appearance,clothing, etc., focusing solely on the object without contextual features.
"""

TYPE_STRUCT_PROMPT_FORMAT = """
Please create the list of attributes for me and return your answer in the following JSON format:
{'attribute1': 'None', 'attribute2': 'None', ...}
"""


OCR_IMAGE_PROMPT = """
fill this json:
    {
        "full_description": full description of the error 
        "key_snippet": "key snippet of the full_description - main objects in the image",
        "background_color": "dominant color in the background"
        "error_message_text": "text of the error message as visible"
        "color_scheme": "primary colors of the device",
        "additional_visual_notes": "any other visually observable details"
    }
"""
