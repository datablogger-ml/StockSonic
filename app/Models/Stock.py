import yfinance as yf


class Stock:
    def __init__(self, stock_name):
        self.ohlc_df = None
        self.stock_name = stock_name

    def fetch_ohlc_data(self, start_date=None, end_date=None):
        self.ohlc_df = yf.download(self.stock_name, start_date, end_date)
