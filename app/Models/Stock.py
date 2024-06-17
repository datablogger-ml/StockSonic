import yfinance as yf


class Stock:
    def __init__(self, stock_name):
        """

        :param stock_name:
        """
        self.rsi_df = None
        self.ohlc_df = None
        self.stock_name = stock_name

    def fetch_ohlc_data(self, start_date=None, end_date=None):
        """

        :param start_date:
        :param end_date:
        :return:
        """
        self.ohlc_df = yf.download(self.stock_name, start_date, end_date)

    def create_rsi_signals(self, timeframe=14):
        """
        
        :param timeframe:
        :return:
        """
        rsi_signal_df = self.ohlc_df.copy()
        gain_loss = rsi_signal_df["CH_CLOSING_PRICE"] - rsi_signal_df["CH_PREVIOUS_CLS_PRICE"]
        rsi_signal_df.loc[gain_loss >= 0, "GAIN"] = gain_loss
        rsi_signal_df.loc[gain_loss < 0, "LOSS"] = gain_loss
        rsi_signal_df[["GAIN", "LOSS"]] = rsi_signal_df[["GAIN", "LOSS"]].fillna(0)
        rsi_signal_df["AVG_GAIN"] = rsi_signal_df["GAIN"].rolling(timeframe).mean().abs()
        rsi_signal_df["AVG_LOSS"] = rsi_signal_df["LOSS"].rolling(timeframe).mean().abs()
        rsi_signal_df["RELATIVE_STRENGTH"] = rsi_signal_df["AVG_GAIN"] / d["AVG_LOSS"]
        rsi_signal_df["RSI"] = 100 - (100 / (1 + rsi_signal_df["RELATIVE_STRENGTH"]))
