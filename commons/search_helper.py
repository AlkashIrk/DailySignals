def case_insensitive(target: dict,
                     search_attribute: str,
                     upper: bool = True,
                     lower: bool = False,
                     default_value=None,
                     ):
    """
    Регистронезависимый поиск в словаре
    :param target: словарь по которому производится поиск
    :param search_attribute: ключ-атрибут по которому производится поиск
    :param upper: приводить ли ключи в словаре\у атрибута к верхнему регистру
    :param lower: приводить ли ключи в словаре\у атрибута к нижнему регистру
    :param default_value: значение по умолчанию, если поиск был неуспешен
    :return:
    """
    result = default_value
    if upper:
        target = {k.upper(): v for k, v in target.items()}
        result = target.get(search_attribute.upper(), default_value)
    elif lower:
        target = {k.lower(): v for k, v in target.items()}
        result = target.get(search_attribute.lower(), default_value)

    return result
