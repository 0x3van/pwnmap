import re

from typing import Union

from .colors import Colors


class ColorizableElement:
    TITLE = 'title'
    KEYS = 'keys'
    BORDER = 'border'
    BULLET = 'bullet'
    COLUMNS = 'columns'


class BoxChar:
    SPACE = ' '
    """ literally just a space """

    THIN = {
        'vertical'      : '│',
        'horizontal'    : '─',
        'upper_right'   : '┐',
        'upper_left'    : '┌',
        'lower_right'   : '┘',
        'lower_left'    : '└'
    }
    """ thin border charset """

    THICK = {
        'vertical'      : '║',
        'horizontal'    : '═',
        'upper_right'   : '╗',
        'upper_left'    : '╔',
        'lower_right'   : '╝',
        'lower_left'    : '╚'
    }
    """ thicc border charset """

    def __init__(self, thick: bool = False):
        charset = self.THICK if thick is True else self.THIN

        for k, v in charset.items():
            setattr(self, k.upper(), v)


class BoxUtil:

    DEFAULT_COLOR_PALETTE = {
        ColorizableElement.TITLE    : '',
        ColorizableElement.KEYS     : Colors.Bright.CYAN,
        ColorizableElement.BORDER   : Colors.Dark.CYAN,
        ColorizableElement.BULLET   : '',
        ColorizableElement.COLUMNS  : {}
    }

    @staticmethod
    def make_colors(*, title: str = '', keys: str = '', border: str = '', bullet: str = '', **columns) -> dict:
        colors = {
            ColorizableElement.TITLE: title,
            ColorizableElement.KEYS: keys,
            ColorizableElement.BORDER: border,
            ColorizableElement.BULLET: bullet,
            ColorizableElement.COLUMNS: {}
        }

        for k, v in columns.items():
            if not isinstance(k, int) or int(k) < 0:
                raise Exception('Invalid column: %s' % str(k))

            colors[ColorizableElement.COLUMNS] |= {k: v}

        return colors

    @staticmethod
    def colorize(text: str, k: Union[str, int], colors: dict) -> str:
        color = colors.get(ColorizableElement.COLUMNS, {}).get(k, '') if isinstance(k, int) else colors.get(k, '')
        return color + text + (Colors.RESET if len(color) > 0 else '')

    @staticmethod
    def strip_ansi(text: str) -> str:
        return re.sub('\x1b' + r'\[(\d(;|))+m', '', text)

    @staticmethod
    def spaces(n: int) -> str:
        return BoxChar.SPACE * n

    @classmethod
    def boxify(cls, iterator: Union[list, tuple], *, title: str = None, spacing: int = 1, sep: str = ' ', bullet: str = '', show_keys: bool = False, colors: dict = DEFAULT_COLOR_PALETTE, thicc_border: bool = False):
        boxchar = BoxChar(thicc_border)

        if isinstance(iterator, list) or isinstance(iterator, tuple):            
            items = []

            # cast all keys and values in each dictionary
            # in list to to string type.
            for dict_item in iterator:
                _dict_item = {}
                for k, v in dict_item.items():
                    _dict_item |= {str(k): str(v)}
                items.append(_dict_item)

            # get the maximum amount of entries in the dictionary list
            dict_item_max_entries = 0

            for dict_item in items:
                if len(dict_item.values()) > dict_item_max_entries:
                    dict_item_max_entries = len(dict_item.values())

            dict_item_max_entry_lens = [0 for _ in range(dict_item_max_entries)]
            dict_item_all_keys = []

            for dict_item in items:
                for i, k in enumerate(dict_item.keys()):
                    if not k in dict_item_all_keys:
                        dict_item_all_keys.append(k)

                for i in range(len(dict_item.values())):
                    v = list(dict_item.values())[i]
                    k = list(dict_item.keys())[i]

                    if v is not None:
                        if len(v) > dict_item_max_entry_lens[i]:
                            dict_item_max_entry_lens[i] = len(v)

                        if len(k) > dict_item_max_entry_lens[i]:
                            dict_item_max_entry_lens[i] = len(k)

            lines = []

            # add element keys
            if show_keys:
                current_line = cls.spaces(len(bullet))

                for i, k in enumerate(dict_item_all_keys):
                    current_line_spaces = cls.spaces(dict_item_max_entry_lens[i] - len(k))
                    current_line += cls.colorize(k, ColorizableElement.KEYS, colors) + current_line_spaces

                    if i < len(dict_item_max_entry_lens) - 1:
                        current_line += cls.spaces(spacing + len(sep) + spacing)

                lines.append(current_line)
                lines.append(cls.spaces(len(cls.strip_ansi(current_line))))

            # add element values
            for dict_item in items:
                current_line = cls.colorize(bullet, ColorizableElement.BULLET, colors)

                for i, (k, v) in enumerate(dict_item.items()):
                    current_line_spaces = cls.spaces(dict_item_max_entry_lens[i] - len(v))

                    current_line += cls.colorize(v, i, colors) + current_line_spaces

                    if i < len(dict_item_max_entry_lens) - 1:
                        current_line += cls.spaces(spacing) + sep + cls.spaces(spacing)

                lines.append(current_line)

            max_line_len = 0

            for line in lines:
                line = cls.strip_ansi(line)

                if len(line) > max_line_len:
                    max_line_len = len(line)

            # add title
            if title is not None:
                title_spaces = cls.spaces(max_line_len - len(title)) if max_line_len > len(title) else ''

                lines.insert(0, cls.colorize(title, ColorizableElement.TITLE, colors) + title_spaces)
                lines.insert(1, boxchar.HORIZONTAL * len(title) + title_spaces)

            # add border
            for i in range(len(lines)):
                line = ''
                line += cls.colorize(boxchar.VERTICAL, ColorizableElement.BORDER, colors)
                line += boxchar.SPACE + lines[i] + boxchar.SPACE
                line += cls.colorize(boxchar.VERTICAL, ColorizableElement.BORDER, colors)

                lines[i] = line

            border_line = boxchar.HORIZONTAL * (max_line_len + 2)  # +2 = spaces between content and border

            lines.insert(0, cls.colorize(boxchar.UPPER_LEFT + border_line + boxchar.UPPER_RIGHT, ColorizableElement.BORDER, colors))
            lines.insert(len(lines), cls.colorize(boxchar.LOWER_LEFT + border_line + boxchar.LOWER_RIGHT, ColorizableElement.BORDER, colors))

            #comment = 'This is a comment'
            #lines.append(cls.spaces(max_line_len + 4 - len(comment)) + '\x1b[90m' + comment + '\x1b[0m')

            # print box
            print('\n'.join(lines))

        else:
            raise ValueError('type \'%s\' not supported' % iterator.type())
