GET_FULL_DESCRIPTION = """
    Please provide a comprehensive and detailed description of the following image. Focus on identifying and explaining
    all visible elements, including objects, people, their actions, and interactions. Describe the setting, including
    any background details, lighting, and atmosphere. Highlight any emotions or moods conveyed by the scene or the
    subjects within it. Also, mention the style and artistic elements if applicable, such as color palette, composition,
    and any notable textures or patterns. Offer insights into the possible context or story behind the image, including
    cultural or historical references if identifiable.
"""

LIST_OF_OBJECTS_PROMPT = """
"Please analyze the following text and list all objects mentioned individually.
If there are multiple objects of the same type, append an index number to each one.
If it is only one object of the type do not add index.
for example instead of "3 chairs" return "chair1" , "chair2" and "chair3" 
return the list in a JSON format: 
[
    {
    "object": the object - each object individually, if there is more then one of this object add an index,
    "type_of_object" : like person, animal,furniture ect.do not return just "object" as type,give more descriptive type,
    }...
]
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

JSON_STRUCT_PROMPT = """
I have a {object_type} object in the image. I want to collect all the information about an object of this type so that I can
recreate it with maximum fidelity in AI image generators. Prepare for me a list of attributes that I need to fill out
for an object of this type. Give me the list in JSON format ready for submission, give me empty JSON,
do not fill the values. Do not add comments to the json
"""
