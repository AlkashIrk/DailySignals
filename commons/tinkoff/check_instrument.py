from tinkoff.invest import InstrumentIdType

from commons.tinkoff.api_v2 import authorize
from model.config.Config import Config
from model.data_structure.AuthData import AuthData
from model.data_structure.Instrument import Instrument


def get_instrument(
        instrument: Instrument):
    """
    Получение информации об инструменте
    :param instrument: запрашиваемый инструмент
    :return:
    """
    auth = AuthData(token=Config().tinkoff_token)
    with authorize(auth=auth) as client:

        try:
            response = client.instruments.get_instrument_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                id=instrument.figi
            )
        except Exception as e:
            print("Возникла ошибка при проверке инструмента: " + str(instrument))
            print("\t%s" % e)
            return None
        return instrument
