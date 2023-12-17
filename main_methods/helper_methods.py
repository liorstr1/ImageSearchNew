import json
import os


def try_get_description(description_path):
    if not os.path.exists(description_path):
        return None
    try:
        with open(description_path, "r") as f:
            return f.read()
    except Exception as e:
        print(e.args)
        return None


def try_get_data_from_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        print(e.args)
        return None


def save_full_description(description_path, full_description):
    with open(description_path, 'w') as f:
        f.write(full_description)


def save_data_to_json(path, obj):
    with open(path, 'w') as f:
        json.dump(obj, f)
