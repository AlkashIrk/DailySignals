from datetime import datetime

from flask import Flask


def init_filters(app: Flask):
    @app.template_filter('ctime')
    def from_timestamp(obj):
        from pytz import timezone
        import pandas
        if isinstance(obj, pandas.Timestamp):
            ts = obj.value / 10e8
        else:
            ts = int(obj)

        return (datetime.fromtimestamp(ts)
                .astimezone(tz=timezone('Europe/Moscow'))
                .strftime('%Y-%m-%d %H:%M:%S'))

    @app.context_processor
    def inject_today_date():
        return {'today_year': str(datetime.today().year)}
