from commons.search_helper import case_insensitive
from model.signals import Indicator
from model.signals.Attributes import Attributes


def _get_attr_rules(rule: dict, attr_prefix: str) -> dict:
    rules = {}
    attr = case_insensitive(target=rule,
                            search_attribute=attr_prefix + Attributes.ind_value
                            )
    attr_l_band = case_insensitive(target=rule,
                                   search_attribute=attr_prefix + Attributes.ind_l_band
                                   )
    attr_h_band = case_insensitive(target=rule,
                                   search_attribute=attr_prefix + Attributes.ind_h_band
                                   )
    if attr is not None:
        rules.update({attr_prefix + Attributes.ind_value: attr})

    if attr_l_band is not None:
        rules.update({attr_prefix + Attributes.ind_l_band: attr_l_band})

    if attr_h_band is not None:
        rules.update({attr_prefix + Attributes.ind_h_band: attr_h_band})

    return rules


class Trigger:
    # вес триггера
    weight: int
    # имя индикатора к которому относится триггер
    indicator_name: str

    # набор правил для предыдущего значения
    prev_rules: dict = None
    # набор правил для текущего значения
    current_rules: dict = None
    # набор правил для сравнения
    compare_rules: dict = None

    # # набор правил для канальных индикаторов
    # # набор правил для предыдущего нижнего значения
    # prev__rules: dict = None
    # # набор правил для текущего нижнего значения
    # current_rules: dict = None
    # # набор правил для предыдущего верхнего значения
    # prev_rules: dict = None
    # # набор правил для текущего верхнего значения
    # current_rules: dict = None

    # индикатор
    indicator: Indicator

    # сообщение
    message: str

    # сообщение из конфигурации
    yaml_message: str = None

    _values = {}
    _condition = ""

    def __init__(self,
                 indicator_name: str,
                 weight: int,
                 rule: dict
                 ):
        self.indicator_name = indicator_name
        self.weight = weight

        self.yaml_message = case_insensitive(target=rule, search_attribute=Attributes.message)

        self.prev_rules = _get_attr_rules(rule=rule, attr_prefix=Attributes.prev)
        self.current_rules = _get_attr_rules(rule=rule, attr_prefix=Attributes.current)

        self.compare_rules = case_insensitive(target=rule, search_attribute=Attributes.compare)

    def check_indicator(self, indicator: Indicator) -> int:
        """
        Проверка индикатора
        :param indicator:
        :return:
        """
        self.indicator = indicator

        # проверка правил по предыдущим значениям
        prev_conditions = self.__check_value(rules=self.prev_rules,
                                             place=Attributes.prev,
                                             attr_name=Attributes.ind_value,
                                             indicator_column_name=self.indicator.signal_name)
        # нижняя граница для канальных индикаторов
        prev_l_band_conditions = self.__check_value(rules=self.prev_rules,
                                                    place=Attributes.prev,
                                                    attr_name=Attributes.ind_l_band)
        # верхняя граница для канальных индикаторов
        prev_h_band_conditions = self.__check_value(rules=self.prev_rules,
                                                    place=Attributes.prev,
                                                    attr_name=Attributes.ind_h_band)
        #
        prev_s_conditions = prev_conditions and prev_l_band_conditions and prev_h_band_conditions

        # проверка правил по текущим значениям
        current_conditions = self.__check_value(rules=self.current_rules,
                                                place=Attributes.current,
                                                attr_name=Attributes.ind_value,
                                                indicator_column_name=self.indicator.signal_name)
        # нижняя граница для канальных индикаторов
        current_l_band_conditions = self.__check_value(rules=self.current_rules,
                                                       place=Attributes.current,
                                                       attr_name=Attributes.ind_l_band)
        # верхняя граница для канальных индикаторов
        current_h_band_conditions = self.__check_value(rules=self.current_rules,
                                                       place=Attributes.current,
                                                       attr_name=Attributes.ind_h_band)

        current_s_conditions = current_conditions and current_l_band_conditions and current_h_band_conditions

        compare_conditions = self.__compare_values(indicator, self.compare_rules)

        if prev_s_conditions and current_s_conditions and compare_conditions:
            return self.weight

        return 0

    def get_message(self):
        if self.yaml_message is None:
            return self.message
        return self.yaml_message

    def __check_value(self, rules: dict,
                      place: str,
                      attr_name: str = "",
                      indicator_column_name: str = None):

        attribute = place + attr_name
        rule = rules.get(attribute)

        if rule is None:
            return True

        indicator_name = attribute
        if indicator_column_name is not None:
            indicator_name = indicator_column_name

        ind_val = self.indicator.get_attribute(indicator_name)
        value = ind_val.get(place)

        self.message = "{prev:0.{accuracy}f} {arrow} {current:0.{accuracy}f}".format(
            prev=ind_val.get(Attributes.prev),
            current=ind_val.get(Attributes.current),
            accuracy=self.indicator.round_var,
            arrow=Attributes.arrow_sign_utf8,
        )

        if rule.get(Attributes.lower) is not None:
            return value < rule.get(Attributes.lower)

        if rule.get(Attributes.lower_or_equal) is not None:
            return value <= rule.get(Attributes.lower_or_equal)

        if rule.get(Attributes.upper) is not None:
            return value > rule.get(Attributes.upper)

        if rule.get(Attributes.upper_or_equal) is not None:
            return value >= rule.get(Attributes.upper_or_equal)

    def __compare_values(self, indicator: Indicator, rules: dict):
        if rules is None:
            return True

        result = True

        for rule in rules:
            str_condition: str = rules.get(rule).lower()
            value = self.__parse_condition(indicator, str_condition)
            result = result & value

        return result

    def __parse_condition(self, indicator: Indicator, condition: str) -> bool:
        value = True
        lower_ = False
        upper_ = False
        equal_ = False

        self._values = {}

        self._condition = condition.replace(" ", "")
        self.message = condition

        self.__fill_if_found(attribute=Attributes.prev + Attributes.ind_value,
                             place=Attributes.prev,
                             indicator_column_name=self.indicator.signal_name)

        self.__fill_if_found(attribute=Attributes.prev + Attributes.ind_l_band,
                             place=Attributes.prev,
                             indicator_column_name=self.indicator.signal_name + Attributes.ind_l_band)

        self.__fill_if_found(attribute=Attributes.prev + Attributes.ind_h_band,
                             place=Attributes.prev,
                             indicator_column_name=self.indicator.signal_name + Attributes.ind_h_band)

        self.__fill_if_found(attribute=Attributes.current + Attributes.ind_value,
                             place=Attributes.current,
                             indicator_column_name=self.indicator.signal_name)

        self.__fill_if_found(attribute=Attributes.current + Attributes.ind_l_band,
                             place=Attributes.current,
                             indicator_column_name=self.indicator.signal_name + Attributes.ind_l_band)

        self.__fill_if_found(attribute=Attributes.current + Attributes.ind_h_band,
                             place=Attributes.current,
                             indicator_column_name=self.indicator.signal_name + Attributes.ind_h_band)

        self.__fill_if_found(attribute=Attributes.price_current, place=Attributes.prev,
                             indicator_column_name=Attributes.price_close)
        self.__fill_if_found(attribute=Attributes.price_prev, place=Attributes.current,
                             indicator_column_name=Attributes.price_close)

        lower_or_equal_ = condition.find(Attributes.lower_or_equal_) != -1
        upper_or_equal_ = condition.find(Attributes.upper_or_equal_) != -1

        if not lower_or_equal_:
            lower_ = condition.find(Attributes.lower_) != -1

        if not upper_or_equal_:
            upper_ = condition.find(Attributes.upper_) != -1

        if not lower_or_equal_ and not upper_or_equal_:
            equal_ = condition.find(Attributes.equal_) != -1

        value_a = self._values.get("value_a")
        value_b = self._values.get("value_b")

        if equal_:
            self.__prepare_message(Attributes.equal_)
            return value_a == value_b
        elif upper_:
            self.__prepare_message(Attributes.upper_sign_utf8)
            return value_a > value_b
        elif upper_or_equal_:
            self.__prepare_message(Attributes.upper_or_equal_sign_utf8)
            return value_a >= value_b
        elif lower_:
            self.__prepare_message(Attributes.lower_sign_utf8)
            return value_a < value_b
        elif lower_or_equal_:
            self.__prepare_message(Attributes.lower_or_equal_sign_utf8)
            return value_a <= value_b

        return value

    def __fill_if_found(self,
                        attribute: str,
                        place: str,
                        indicator_column_name: str):

        result = self._condition.find(attribute)
        if result == -1:
            return

        ind_value = self.indicator.get_attribute(indicator_column_name).get(place)

        if result == 0:
            self._values.update({"value_a": ind_value})
        else:
            self._values.update({"value_b": ind_value})

    def __prepare_message(self, sign: str):
        self.message = "{value_a} {sign} {value_b}".format(
            value_a=self._values.get("value_a"),
            value_b=self._values.get("value_b"),
            sign=sign,
        )
