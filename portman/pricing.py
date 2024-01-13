import yfinance as yf
import csv
from typing import List, Dict

def latest_closing(ticker: str) -> float:
    """Using Yahoo api via yfinance package to get prices"""
    security_info = yf.Ticker(ticker).history(period="id")
    return security_info["Close"].iloc[-1]

def latest_closing_multiple(tickers: List) -> Dict:
    prices = dict()
    for ticker in tickers:
        prices[ticker] = latest_closing(ticker)
    return prices

def load_raw_ticker_from_csv(path: str, column: str = 'Ticker') -> List:
    offset = None
    ticker_list = list()
    with open(path, 'r') as csvfile:
        reader_variable = csv.reader(csvfile, delimiter=';')
        for row in reader_variable:
            if offset is None: # finding what is the column number based on name
                if row.count(column) > 1:
                    raise KeyError("Specified column appears multiple times in csv!")
                else:
                    offset = row.index(column)
            else:
                ticker_list.append(row[offset])
    return ticker_list

def remove_invalid_tickers(tickers: List ) -> List:
    curated_list = list()
    for ticker in tickers:
        if ticker not in ['-', '']:
            curated_list.append(ticker)
    return curated_list

def save_prices_to_csv(file_name: str, prices: Dict) -> None:
    col_header_dict = dict(**{"Ticker": "Closing price"}, **prices)
    print(col_header_dict)
    with open(file_name, 'w') as file:
        for k, v in col_header_dict.items():
            file.write(f"{k}, {v}\n")
        print(f"{len(prices)} prices saved to {file_name}")

def csv_to_csv_lookup(input:str, output: str, input_col: str = 'Ticker') -> None:
    """Using ticker input from csv file from specified column, saving ticker:price pairs to another csv."""
    raw_input = load_raw_ticker_from_csv(input, input_col)
    price_dict = latest_closing_multiple(remove_invalid_tickers(raw_input))
    save_prices_to_csv(output, price_dict)


if __name__ == "__main__":
    csv_to_csv_lookup("test1.csv", "testout1.csv")

    # tickers = ['SXR8.BD', 'LYMS.DE']
    # get_prices(tickers, "test.csv")