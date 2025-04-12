from flask import Flask, render_template

from flask_app.flask_data import prepare_instruments, prepare_candles, prepare_candles_ticker


def init_views(app: Flask):
    @app.route('/')
    def index():
        return render_template('index.html',
                               index_page=True
                               )

    @app.route('/instruments')
    def instruments():
        df = prepare_instruments()
        records = df.to_dict('records')
        col_names = list(df.columns)
        if 'id' in col_names:
            col_names.remove('id')
            col_names.remove('is_trade')

        return render_template('instruments.html',
                               records=records,
                               colnames=col_names,
                               instruments_page=True
                               )

    @app.route('/candles')
    def candles():
        df = prepare_candles()
        records = df.to_dict('records')
        col_names = list(df.columns)
        if 'id' in col_names:
            col_names.remove('id')
        return render_template('candles.html',
                               records=records,
                               colnames=col_names,
                               candles_page=True
                               )

    @app.route('/candles/<page_id>')
    def candlesId(page_id):
        df = prepare_candles_ticker(page_id)
        records = df.to_dict('records')
        col_names = list(df.columns)
        if 'id' in col_names:
            col_names.remove('id')
            col_names.remove('name')
            col_names.remove('ticker')
        return render_template('candles_instrument.html',
                               instrument=df.iloc[0]["name"],
                               ticker=df.iloc[0]["ticker"],
                               records=records,
                               colnames=col_names,
                               candles_page=False
                               )
