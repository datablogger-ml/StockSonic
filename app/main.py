from datetime import datetime, timedelta

from app.Models.Stock import Stock
from app.plots.figures import chart_rsi


if __name__ == "__main__":
    input_name = "MSFT"
    start_date = "2024-01-01"
    end_date = "2024-06-01"

    # incremental_amount = 10_000
    # bollinger_timeframe = 20
    # std_deviation_multiplier = 2
    # raw_data_list = []
    # trade_df_list = []

    rsi_timeframe = 14

    rsi_upper_cap = 80
    rsi_lower_cap = 30

    my_stock = Stock(input_name)
    my_stock.fetch_ohlc_data(start_date, end_date)
    print(my_stock.ohlc_df)
    my_stock.create_rsi_signals(rsi_timeframe)
    print(my_stock.rsi_df)
    # Charting RSI
    chart_rsi('RSI', my_stock.rsi_df)

