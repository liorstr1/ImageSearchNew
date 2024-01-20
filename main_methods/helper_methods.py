import json
import os
import inflect as inflect


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


def break_down_count(list_of_objects):
    def split_plural_objects(data):
        sing = p.singular_noun(data['object'])
        count = data.get('object_count', 0)
        for idx in range(1, count + 1):
            new_name = f'{sing}_{idx}'
            res.append(
                {
                    'object': new_name,
                    'object_type': sing,
                    'count': 1
                }
            )
    res = []
    p = inflect.engine()
    for o in list_of_objects:
        if o['object_count'] == 1:
            res.append(
                {
                    'object': o['object'],
                    'object_type': o['object'],
                    'object_count': 1,
                }
            )
        else:
            split_plural_objects(o)
    return res
