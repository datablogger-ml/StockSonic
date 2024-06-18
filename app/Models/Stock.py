import yfinance as yf


class Stock:
    def __init__(self, stock_name):
        """
        This class is used to fetch stock data from Yahoo Finance API
        :param stock_name: The name of the stock
        """
        self.shares_held = None
        self.total_loss_or_gain = None
        self.rsi_signal = None
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

    def create_buy_sell_signal_rsi(self, upper_level=70, lower_level=30):
        """
        Calculate the buy and sell signals based on the RSI column.

        :param upper_level: The upper level of RSI to trigger a sell signal. Default is 70.
        :param lower_level: The lower level of RSI to trigger a buy signal. Default is 30.
        :return: A DataFrame with the buy and sell signals.
        """
        signals_df = self.rsi_df.copy(deep=True)
        signals_df['BUY_SIGNAL'] = np.where(signals_df['RSI'] < lower_level, 1, 0)
        signals_df['SELL_SIGNAL'] = np.where(signals_df['RSI'] > upper_level, -1, 0)
        self.rsi_signal = signals_df

    def calculate_rsi_trade(self, shares_bought, holding_period=30):
        """
        Calculate the total loss or gain based on the number of shares brought, taking into account the buy and sell
        signals and a minimum holding period of 30 days.

        :param shares_bought: The number of shares bought.
        :param holding_period: The minimum holding period in days. Default is 30.
        :return: A tuple containing the total loss or gain and the number of shares held at the end of the holding
        period.
        """
        self.total_loss_or_gain = 0
        self.shares_held = shares_bought

        for i in range(holding_period, len(self.rsi_df)):
            if self.rsi_df.loc[i, 'BUY_SIGNAL'] == 1 and self.shares_held == 0:
                self.shares_held = shares_bought
            elif self.rsi_df.loc[i, 'SELL_SIGNAL'] == -1 and self.shares_held > 0:
                self.total_loss_or_gain += self.rsi_df.loc[i, 'CLOSE'] * self.shares_held
                self.shares_held = 0
