# coding=utf-8


"""字段名称映射"""
_FIELD_NAME_MAP = [
    ['price', 'close'],
    ['pt_price', 'pt_close'],
    ['prev_price', 'prev_close'],
    ['money', 'amount']
]


def translate_field_name(fields, reverse=False):
    """字段名称映射"""
    if fields is None:
        return None, False

    if not isinstance(fields, str):
        anyone_changed = False
        new_fields = []
        for field in fields:
            new_field, changed = translate_field_name(field, reverse=reverse)
            new_fields.append(new_field)
            if changed:
                anyone_changed = True

        return new_fields, anyone_changed

    if reverse:
        ki = 1
        vi = 0
    else:
        ki = 0
        vi = 1

    field = fields
    for kv in _FIELD_NAME_MAP:
        if kv[ki] == field:
            return kv[vi], True

    return field, False
