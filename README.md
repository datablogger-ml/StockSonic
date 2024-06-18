# StockSonic
StockSonic is a financial blog dedicated to providing insights, analysis, and education about stock market investing. With a team of experienced investors and traders, StockSonic aims to help individuals navigate the complex world of stocks and make informed investment decisions.

The blog covers a wide range of topics, including stock market trends, investment strategies, company analysis, and market news. Whether you're a beginner looking to learn the basics of investing or an experienced investor seeking advanced insights, StockSonic offers valuable information and resources to enhance your investment knowledge.

Through in-depth articles, expert interviews, and educational resources, StockSonic strives to empower individuals to take control of their financial future and achieve their investment goals. Join the StockSonic community today and dive into the exciting world of stock market investing.

### Stock Class
The Stock class in Models/Stock.py is designed to fetch stock data from the Yahoo Finance API. It provides the following functionalities:

* **Initialization**:
  * __init__(self, stock_name): Initializes the Stock object with the provided stock_name.
* **Data Fetching**:
  * fetch_ohlc_data(self, start_date=None, end_date=None): Fetches OHLC (Open, High, Low, Close) data for the stock within the specified date range.
* **RSI Calculation**:
  * create_rsi_signals(self, timeframe=14): Calculates Relative Strength Index (RSI) signals based on the fetched OHLC data.
* **Buy/Sell Signal Generation**:
  * create_buy_sell_signal_rsi(self, upper_level=70, lower_level=30): Generates buy and sell signals based on RSI values.
* **Trade Calculation**:
  * calculate_rsi_trade(self, shares_bought, holding_period=30): Calculates total loss or gain based on buy and sell signals over a specified holding period.