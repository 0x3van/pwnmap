from typing import Union


class HTMLUtil:

    @staticmethod
    def get_element_string(target, *elems) -> Union[str, None]:
        for elem in elems:
            if isinstance(elem, tuple):
                name, attrbs = elem
            else:
                name = elem
                attrbs = {}

            target = target.find(name, attrbs)

            if target is None:
                return None

        return target.text.strip()
