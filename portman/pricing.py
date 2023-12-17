import yfinance as yf
import csv
from typing import List, Dict

def get_closing_price(ticker: str) -> float:
    """Using Yahoo api via yfinance package to get prices"""
    security = yf.Ticker(ticker)
    hist = security.history(period="id")
    closing_price = hist["Close"].iloc[-1]
    return closing_price

def get_prices_for_list(ticker_list: List) -> Dict:
    table = dict()
    for ticker in ticker_list:
        price = get_closing_price(ticker)
        table[ticker] = price
    return table

def prices_to_csv(file_name: str, prices: Dict) -> None:
    field_names = ["Ticker", "Closing price"]
    with open(file_name, 'w') as file:
        for k, v in prices.items():
            file.write(f"{k}, {v}\n")
        print(f"{len(prices)} prices saved to {file_name}")

def get_prices(ticker_list: List, filename=None) -> None:
    prices = get_prices_for_list(ticker_list)
    if filename:
        prices_to_csv(filename, prices)
    else:
        print(prices)

tickers = ['SXR8.BD', 'LYMS.DE']
get_prices(tickers, "test.csv")