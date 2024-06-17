import yfinance as yf
import matplotlib.pyplot as plt


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
        
        # Formatting Columns as required
        self.ohlc_df.columns = self.ohlc_df.columns.str.upper()
        self.ohlc_df.reset_index(inplace=True)

    def create_rsi_signals(self, timeframe=14):
        """

        :param timeframe:
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

    def chart_rsi(self, title, df):
        """

        :param title:
        :param df:
        :return:
        """
        plt.figure()
        fig, ax = plt.subplots()
        ax.set_title(title)
        fig.subplots_adjust(bottom=0.2)
        ax.plot(df['Date'], df['RSI'])
        ax.set_ylim(0, 100)
        ax.axhline(y=70, color='r', linestyle='-')
        ax.axhline(y=30, color='r', linestyle='-')
        ax.grid(True)
        ax.set_ylabel(r'RSI')
        for label in ax.get_xticklabels(which='major'):
            label.set(rotation=30, horizontalalignment='right')
        plt.show()
