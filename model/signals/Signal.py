import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

import yaml

from commons.search_helper import case_insensitive
from commons.сurrency_symbol import get_symbol
from model.config.Config import Config
from model.data_structure.Instrument import Instrument
from model.signals import *
from model.signals.Attributes import Attributes
from model.signals.PandasData import PandasData
from model.signals.Trigger import Trigger


@dataclass
class Signal:
    all_indicators: list
    used_indicators: set
    min_weight: int
    signal_triggers: dict
    signal_description: str = None

    def __init__(self):
        self.all_indicators = []
        self.min_weight = 1
        self.signal_triggers = {}
        self.used_indicators = set()

    def read_config(self, file_path: str = None):
        """
        Чтение конфигурации для расчета сигналов по индикаторам
        :param file_path:
        :return:
        """
        self.__get_indicators()
        yaml_cfg = {}

        if file_path is None:
            file_path = Config().config_signals_path

        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding="UTF-8") as file:
                yaml_cfg = yaml.safe_load(file)

            self.__parse_yaml(cfg=yaml_cfg)
        else:
            text = "YAML файл конфигурации сигналов не обнаружен.\nОжидаемое место расположения файла:\n\t{path}" \
                .format(path=os.path.abspath(file_path))
            print(text)
        return self

    def check_signals(self, pd: PandasData) -> List[Trigger]:
        """
        Подсчет сигналов по инструменту
        :param pd:
        :return: Коллекция сигналов давших положительный результат
        """

        # сумма по сигналам
        width_triggered = 0
        # список сработовших сигналов
        triggered_signals = []

        for indicator in Indicator.__subclasses__():
            skip_if_has_signal = False

            # если индикатор есть в конфигурации
            if indicator.signal_name in self.used_indicators:
                indicator_values = indicator(data=pd)
                indicator_triggers = self.signal_triggers.get(indicator.signal_name)
                for trigger in indicator_triggers:

                    # если уже есть сигнал по индикатору, больше не учитываем его
                    if skip_if_has_signal:
                        break

                    result = trigger.check_indicator(indicator=indicator_values)
                    width_triggered = width_triggered + result

                    if result != 0:
                        triggered_signals.append(trigger)
                        skip_if_has_signal = True

        # если сумма весов по индикаторам не достигла значения при котором отправляется сигнал, очищаем коллекцию
        if width_triggered < self.min_weight:
            triggered_signals.clear()

        return triggered_signals

    def get_console_message(self, instrument: Instrument, triggered_signals: List[Trigger]):
        level = 0
        tab_char = "\t"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        signal_description = ""

        if self.signal_description is not None:
            level += 1
            signal_description = self.signal_description + "\n"

        instrument_info = tab_char * level + "{name} ({ticker})".format(
            name=instrument.name,
            ticker=instrument.ticker
        )

        price_info = tab_char * level + "Цена: {price}{currency_sign}".format(
            price=instrument.last_price,
            currency_sign=get_symbol(instrument.currency)
        )
        level += 1

        signals = ""
        for trigger in triggered_signals:
            trigger: Trigger = trigger

            tabs_level_1 = tab_char * level
            tabs_level_2 = tab_char * (level + 1)

            signals = signals + "\n{tabs_level_1}{indicator_name}\n{tabs_level_2}{message}".format(
                tabs_level_1=tabs_level_1,
                tabs_level_2=tabs_level_2,
                indicator_name=trigger.indicator_name,
                message=trigger.get_message()
            )

        message = "{time}\n{signal_description} {instrument_info}\n{price_info}\n{signals}\n".format(
            time=current_time,
            signal_description=signal_description,
            instrument_info=instrument_info,
            price_info=price_info,
            signals=signals,
        )

        return message

    def get_tg_message(self, instrument: Instrument, triggered_signals: List[Trigger]):
        level = 0
        tab_char = "\t"
        signal_description = ""
        tinkoff_url = '<a href="https://www.tinkoff.ru/invest/stocks/{ticker}/">{name} ({ticker})</a>'

        if self.signal_description is not None:
            level += 1
            signal_description = self.signal_description + "\n"

        instrument_info = tab_char * level + tinkoff_url.format(
            name=instrument.name,
            ticker=instrument.ticker
        )

        price_info = tab_char * level + "Цена: {price}{currency_sign}".format(
            price=instrument.last_price,
            currency_sign=get_symbol(instrument.currency)
        )
        level += 1

        signals = ""
        for trigger in triggered_signals:
            trigger: Trigger = trigger

            tabs_level_1 = tab_char * level
            tabs_level_2 = tab_char * (level + 1)

            signals = signals + "\n{tabs_level_1}{indicator_name}\n{tabs_level_2}{message}".format(
                tabs_level_1=tabs_level_1,
                tabs_level_2=tabs_level_2,
                indicator_name=trigger.indicator_name,
                message=trigger.get_message()
            )

        message = "{signal_description}{instrument_info}\n{price_info}\n{signals}\n".format(
            signal_description=signal_description,
            instrument_info=instrument_info,
            price_info=price_info,
            signals=signals,
        )

        return message

    def __get_indicators(self):
        """
        Определяем какие индикаторы могут использоваться
        :return:
        """
        self.all_indicators = []

        for t in Indicator.__subclasses__():
            self.all_indicators.append(t.signal_name)

    def __parse_yaml(self, cfg: dict):
        """
        Парсинг YAML конфигурации для расчета сигналов по индикаторам
        :param cfg:
        :return:
        """
        main_section: dict = case_insensitive(target=cfg,
                                              search_attribute=Attributes.main_section,
                                              default_value={}
                                              )

        self.min_weight: int = case_insensitive(target=main_section,
                                                search_attribute=Attributes.min_weight,
                                                lower=True,
                                                default_value=0
                                                )
        self.signal_description: str = case_insensitive(target=main_section,
                                                        search_attribute=Attributes.signal_description,
                                                        lower=True,
                                                        default_value=None
                                                        )

        # проверяем наличие индикатора в условиях
        for indicator_name in self.all_indicators:
            # пробуем получить условия по индикатору
            conditions: dict = case_insensitive(target=cfg,
                                                search_attribute=indicator_name
                                                )

            # если заданы условия по индикатору сохраняем их в памяти
            if conditions is not None:
                # вес индикатора
                indicator_weight: int = case_insensitive(target=conditions,
                                                         search_attribute=Attributes.weight,
                                                         lower=True,
                                                         default_value=1
                                                         )

                # пробуем получить набор правил по индикатору
                rules: dict = case_insensitive(target=conditions,
                                               search_attribute=Attributes.rules,
                                               lower=True,
                                               default_value={}
                                               )

                for rule in rules:
                    trigger = Trigger(indicator_name=indicator_name,
                                      weight=indicator_weight,
                                      rule=rules.get(rule)
                                      )

                    # пробуем получить список тригеров по индикатору
                    indicator_triggers = self.signal_triggers.get(indicator_name, [])
                    indicator_triggers.append(trigger)

                    # обновляем список тригеров по индикатору
                    self.signal_triggers.update({indicator_name: indicator_triggers})
                    # обновляем Set используемых индикаторов
                    self.used_indicators.add(indicator_name)
