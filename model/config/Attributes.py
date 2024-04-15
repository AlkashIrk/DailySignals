class Attributes:
    main_section = "main"
    subs_section = "subscription"

    # region метки для раздела Main
    # токен от investAPI
    tinkoff_token = "tinkoff_token"

    # токен от телеграма
    telegram_token = "telegram_token"
    # endregion

    # region метки для раздела Subscription
    # подписка на свечи
    interval = "interval"

    # интервал (в минутах) для расчета сигналов
    calculate_signals_interval = "calculate_signals_interval"

    # минимальное количество свечей для расчета
    candles_for_calculation_min_size = "candles_for_calculation_min_size"

    # путь до файла конфигурации сигналов
    signals_config_path = "signals_config_path"

    # endregion
