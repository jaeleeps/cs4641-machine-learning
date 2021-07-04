import yfinance as yf
import pandas as pd
from pydantic import BaseModel

import os
import sys

# from src._model.stock_data_interface import YFINANCE_INTERVAL_TYPE


class StockDataLoader:

    @staticmethod
    def test() -> None:
        appl_history = yf.download('AAPL', start='2021-05-01', end='2021-06-01')
        print(appl_history)
        print(type(appl_history))

    @staticmethod
    def get_ticker_history(ticker: str,
                           start: str,
                           end: str,
                           interval: str,
                           action: bool,
                           rounding: bool,
                           ):
        targetTicker: yf.Ticker = yf.Ticker(ticker)
        return targetTicker.history(
            interval=interval,
            start=start,
            end=end,
            action=action,
            rounding=rounding
        )

    @staticmethod
    def get_download_df(ticker: str,
                         start: str,
                         end: str,
                         interval: str,
                         action: bool,
                         rounding: bool,
                         ):
        data_df: pd.DataFrame = yf.download(
            tickers=ticker,
            interval=interval,
            start=start,
            end=end,
            action=action,
            rounding=rounding
        )
        return data_df

    @staticmethod
    def save_pf_as_scv(
            data_df: pd.DataFrame,
            csv_name: str,
            relative_path: str):
        script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
        proj_root_path = os.path.join(script_dir, '../')
        csv_path = os.path.join(proj_root_path, relative_path)
        data_df.to_csv(os.path.join(csv_path, csv_name))
