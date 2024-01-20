import json
import re


def convert_resp(resp):
    resp = remove_text_before_and_after_json(resp)
    res = try_simple(resp)
    if res is None:
        resp_s = remove_backslash_char_num(resp)
        res = try_simple(resp_s)
    if res is None:
        resp_r = resp.replace("}\n{", "},\n{")
        res = try_simple(resp_r)
    if res is None:
        resp_t = resp.replace('{\'', '{"').replace('\':', '":').replace(': \'', ': "').replace('\', \'', '", "').replace('\'}', '"}')
        res = try_simple(resp_t)
    if res is None:
        h = 0
    return res


def try_simple(resp):
    try:
        return json.loads(resp)
    except Exception as e:
        print(e.args)
        return None


def remove_backslash_char_num(string):
    return re.sub(r'\\_', '_', string)


def remove_text_before_and_after_json(resp):
    indices = [(resp.find('['), resp.rfind(']') + 1), (resp.find('{'), resp.rfind('}') + 1)]
    indices = [i for i in indices if i[0] > -1 and i[1] > 0]
    indices = list(sorted(indices, key=lambda x: x[0]))
    resp = resp[indices[0][0]:indices[0][1]]
    return resp


