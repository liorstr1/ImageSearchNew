import os
import json
import re

from openai import OpenAI
import replicate
from prompts.get_data_from_image_prompts import LIST_OF_OBJECTS_PROMPT, GET_COORDINATES_PROMPT, \
    GET_COORDINATES_FROM_TEXT_PROMPT, GET_DESCRIPTION_PROMPT

SYSTEM = 'system'
USER = 'user'
ASSISTANT = 'assistant'


def get_description_from_cogvlm(image_path_url, prompt):
    try:
        output = replicate.run(
            "naklecha/cogvlm:ec3886f9ea85dd0aee216585be5e6d07b04c9650f7b8b08363a14eb89e207eb2",
            input={
                "image":  image_path_url,
                "prompt": prompt
            }
        )
        return output
    except Exception as e:
        print(e.args)
        return None


def get_list_of_objects_from_llama(prompt):
    try:
        output = replicate.run(
            "meta/llama-2-13b:078d7a002387bd96d93b0302a4c03b3f15824b63104034bfa943c63a8f208c38",
            input={
                "debug": True,
                "top_k": 50,
                "top_p": 0.9,
                "prompt": prompt,
                "temperature": 0.75,
                "max_new_tokens": 2048,
                "min_new_tokens": -1
            }
        )
        output_list = list(output)
        return output_list
    except Exception as e:
        print(e.args)
        return None


def get_coordinates_from_llava(image_url, list_of_objects):
    output = replicate.run(
        "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
        input={
            "image": image_url,
            "prompt": GET_COORDINATES_PROMPT.format(list_of_objects=list_of_objects)
        }
    )
    output_text = ""
    for out in output:
        output_text += out

    try:
        res = json.loads(output_text)
    except json.JSONDecodeError as e:
        def remove_backslash_char_num(string):
            # This regular expression finds a backslash (\) followed by a letter and a digit
            return re.sub(r'\\_', '_', string)

        output_string = remove_backslash_char_num(output_text)
        try:
            res = json.loads(output_string)
        except Exception as e:
            print(e.args)
            res = get_list_of_coords_from_gpt4(output_text)
    return {r['object_name']: r['object_coordinates'] for r in res}


def get_response_from_gpt(messages, client):
    response = client.chat.completions.create(
        messages=messages,
        model="gpt-4-1106-preview",
        response_format={"type": "json_object"},
    )
    resp = response.choices[0].message.content
    return json.loads(resp)


def get_list_of_coords_from_gpt4(description):
    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        messages = init_messages(description, GET_COORDINATES_FROM_TEXT_PROMPT)
        return get_response_from_gpt(messages, client)['objects']
    except Exception as e:
        print(e.args)
        return None


def get_list_of_objects_from_gpt4(text_of_coords):
    try:
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        messages = init_messages(text_of_coords, LIST_OF_OBJECTS_PROMPT)
        list_of_objects = get_response_from_gpt(messages, client)['objects']
        messages = update_chat(
            messages,
            ASSISTANT,
            "list of objects:" + ",".join(list_of_objects)
        )
        messages = update_chat(
            messages,
            USER,
            "are you sure all objects are valid objects from the description ? if not update the JSON"
        )
        list_of_objects2 = get_response_from_gpt(messages, client)['objects']
        return list_of_objects2
    except Exception as e:
        print(e.args)
        return None


def update_chat(messages: list, role: str, content: str):
    messages.append({"role": role, "content": content})
    return messages


def init_messages(user_prompt, system_prompt):
    messages = []
    messages = update_chat(messages, SYSTEM, system_prompt)
    messages = update_chat(messages, USER, user_prompt)
    return messages


def get_description_from_llava(image_url, o_object, coords):
    output = replicate.run(
        "yorickvp/llava-13b:e272157381e2a3bf12df3a8edd1f38d1dbd736bbb7437277c8b34175f8fce358",
        input={
            "image": image_url,
            "prompt": GET_DESCRIPTION_PROMPT.format(
                image=image_url,
                coords=coords,
                object=o_object
            )
        }
    )
    output_text = ""
    for out in output:
        output_text += out

    try:
        res = json.loads(output_text)
    except json.JSONDecodeError as e:
        def remove_backslash_char_num(string):
            # This regular expression finds a backslash (\) followed by a letter and a digit
            return re.sub(r'\\_', '_', string)

        output_string = remove_backslash_char_num(output_text)
        try:
            res = json.loads(output_string)
        except Exception as e:
            print(e.args)
            res = get_list_of_coords_from_gpt4(output_text)
    return {r['object_name']: r['object_coordinates'] for r in res}