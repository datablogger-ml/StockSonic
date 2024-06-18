import yfinance as yf


class Stock:
    def __init__(self, stock_name):
        """
        This class is used to fetch stock data from Yahoo Finance API
        :param stock_name: The name of the stock
        """
        self.rsi_df = None
        self.ohlc_df = None
        self.stock_name = stock_name

    def fetch_ohlc_data(self, start_date=None, end_date=None):
        """
        Function to fetch stock data from Yahoo Finance API
        :param start_date: The start date in YYYY-MM-DD
        :param end_date: The end date in YYYY-MM-DD
        :return:
        """
        self.ohlc_df = yf.download(self.stock_name, start_date, end_date)
        
        # Formatting Columns as required
        self.ohlc_df.columns = self.ohlc_df.columns.str.upper()
        self.ohlc_df.reset_index(inplace=True)

    def create_rsi_signals(self, timeframe=14):
        """
        Calculate the Relative Strength Index (RSI) signals for the given OHLC data.

        The RSI is a momentum oscillator that measures the speed and change of price movements.
        It is used to identify overbought and oversold conditions in the market.

        :param timeframe: The number of periods to use for the RSI calculation. Default is 14.
        :return:
        """
        rsi_signal_df = self.ohlc_df.copy(deep=True)

        # Shifting CLOSE by 1 to create Previous day closing price column
        rsi_signal_df['PREV_CLOSE'] = rsi_signal_df['CLOSE'].shift(1)

        # Calculating Gain or Loss for each day
        gain_loss = rsi_signal_df["CLOSE"] - rsi_signal_df["PREV_CLOSE"]
        rsi_signal_df.loc[gain_loss >= 0, "GAIN"] = gain_loss
        rsi_signal_df.loc[gain_loss < 0, "LOSS"] = gain_loss
        rsi_signal_df[["GAIN", "LOSS"]] = rsi_signal_df[["GAIN", "LOSS"]].fillna(0)
        rsi_signal_df["AVG_GAIN"] = rsi_signal_df["GAIN"].rolling(timeframe).mean().abs()
        rsi_signal_df["AVG_LOSS"] = rsi_signal_df["LOSS"].rolling(timeframe).mean().abs()
        rsi_signal_df["RELATIVE_STRENGTH"] = rsi_signal_df["AVG_GAIN"] / rsi_signal_df["AVG_LOSS"]

        # Calculating RSI signal
        rsi_signal_df["RSI"] = 100 - (100 / (1 + rsi_signal_df["RELATIVE_STRENGTH"]))
        self.rsi_df = rsi_signal_df.copy(deep=True)

