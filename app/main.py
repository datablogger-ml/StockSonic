from app.Models.Stock import Stock


if __name__ == "__main__":
    input_name = "MSFT"
    start_date = "2024-01-01"
    end_date = "2024-06-01"

    my_stock = Stock(input_name)
    my_stock.fetch_ohlc_data(start_date, end_date)
    print(my_stock.ohlc_df)
