import yfinance as yf


class Stock:
    def __init__(self, stock_name):
        self.stock_name = stock_name
        self.details = yf.Ticker(self.stock_name)
