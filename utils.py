import re


def get_in(in_dictionary: dict, path: list):
    for p in path:
        in_dictionary = in_dictionary.get(p)
        if in_dictionary is None:
            return None
    return in_dictionary


def slugify(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9 ]", "", value.lower())
