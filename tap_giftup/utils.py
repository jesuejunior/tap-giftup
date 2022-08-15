import os
import re
from dateutil.parser import parse


class SchemaNotSetError(Exception):
    pass


class KeyPropNotSetError(Exception):
    pass


def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def to_snake(s):
  return re.sub('([A-Z]\w+$)', '_\\1', s).lower()


def convert_dict_keys_to_snake(d):
   if isinstance(d, list):
      return [convert_dict_keys_to_snake(i) if isinstance(i, (dict, list)) else i for i in d]
   return {to_snake(a):convert_dict_keys_to_snake(b) if isinstance(b, (dict, list)) else b for a, b in d.items()}
