class Attributes:
    main_section = "signal"
    # минимальный вес для генерации сигнала
    min_weight = "min_weight"
    # описание сигнала
    signal_description = "description"

    # вес сигнала
    weight = "weight"
    # набор правил
    rules = "rules"

    # сообщение для индикатора
    message = "message"

    # предыдущее значение
    prev = "prev"
    # текущее значение
    current = "current"
    # правила для сравнений
    compare = "compare"

    ind_value = "_value"

    # текущая цена
    price_current = "price_current"
    # предыдущая цена
    price_prev = "price_prev"

    # строго меньше чем
    lower = "lower"
    # меньше или равеч чем
    lower_or_equal = "lower_or_equal"

    # строго больше чем
    upper = "upper"
    # больше или равен чем
    upper_or_equal = "upper_or_equal"

    # region Поля-значения для индикаторов
    # закрытие свечи (текущая цена)
    price_close = "close"
    # нижнее значение для канальных индикаторов
    ind_l_band = "_l_band"
    # верхнее значение для канальных индикаторов
    ind_h_band = "_h_band"
    # endregion

    # region Доступные поля-значения для парсинга условий сравнения
    # меньше
    lower_ = "<"
    # меньше или равен
    lower_or_equal_ = "<="
    # больше
    upper_ = ">"
    # больше или равен
    upper_or_equal_ = ">="
    # равен
    equal_ = "="
    # endregion
