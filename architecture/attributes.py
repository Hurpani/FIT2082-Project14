from typing import Union, Dict


class Attributes:
    ATTRIBUTE_TYPE: type = Union[float, int, str]

    def __init__(self, args: [(str, ATTRIBUTE_TYPE)]):
        self.attribute_value_pairs: Dict[str, Attributes.ATTRIBUTE_TYPE] = {}
        self.attributes: [str] = []
        for key_attrib_pair in args:
            self.attribute_value_pairs[key_attrib_pair[0]] = key_attrib_pair[1]
            self.attributes.append(key_attrib_pair[0])

    def get(self, key: str) -> Union[ATTRIBUTE_TYPE, None]:
        if key in self.attribute_value_pairs:
            return self.attribute_value_pairs[key]
        return None

    def set_for(self, obj: object):
        """\
    Updates an object with this Attributes' attributes and values.
        """
        for key in self.attributes:
            obj.key = self.attribute_value_pairs[key]
