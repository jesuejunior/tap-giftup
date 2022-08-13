import os
from dateutil.parser import parse

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


class SchemaNotSetError(Exception):
    pass


class KeyPropNotSetError(Exception):
    pass
