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
return the list in a JSON format: [object, object...]:
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
 give me full description of this object in a way that will help me to reproduce the object in AI image creator
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