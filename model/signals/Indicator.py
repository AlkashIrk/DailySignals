from dataclasses import dataclass

import pandas as pd

from model.signals.Attributes import Attributes


@dataclass
class Indicator:
    df: pd.DataFrame
    signal_name = ""
    calc_time = 0
    previous_value = 0
    current_value = 0
    round_var = 2
    values = {}

    def print_info(self):
        tab_counter = (24 - len(self.signal_name)) // 4

        value = "{signal_name}{tabs}{prev:.2f}\t->\t{current:.2f}\t\t(t={time:.3f} ms)".format(
            signal_name=self.signal_name,
            tabs="\t" * tab_counter,
            prev=self.previous_value,
            current=self.current_value,
            time=round(self.calc_time * 1000, 3)
        )
        print(value)

    def update_values(self):
        self.previous_value = self.__previous_value()
        self.current_value = self.__current_value()

    def __current_value(self):
        return round(self.df[self.signal_name][self.df[self.signal_name].size - 1], self.round_var)

    def __previous_value(self):
        return round(self.df[self.signal_name][self.df[self.signal_name].size - 2], self.round_var)

    def previous_close_value(self):
        return self.df[Attributes.price_close][self.df[Attributes.price_close].size - 2]

    def current_close_value(self):
        return self.df[Attributes.price_close][self.df[Attributes.price_close].size - 1]

    def set_previous_value(self, value):
        self.previous_value = value

    def set_current_value(self, value):
        self.current_value = value

    def get_attribute(self, attribute: str = None) -> dict:
        result = {}

        column_name = self.signal_name
        if attribute is not None:
            column_name = self.signal_name + attribute
        if attribute is not None:
            column_name = attribute

        if column_name in self.df:
            prev = round(self.df[column_name][self.df[column_name].size - 2], self.round_var)
            current = round(self.df[column_name][self.df[column_name].size - 1], self.round_var)

            result.update({Attributes.prev: prev})
            result.update({Attributes.current: current})
        return result
