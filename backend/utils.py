def set_nested(d: dict, keys: list, value) -> None:
    """
    Adds a Value
    :param d: dict
    :param keys: where
    :param value: what to set
    :return:
    """
    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value
