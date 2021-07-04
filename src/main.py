from src.preparation.nyt_data_loader import NytDataLoader
from src.preparation.stock_data_loader import StockDataLoader
from src.preparation.uitl import Util


def download_apple_stock_history():
    target_ticker: str = 'AAPL'
    start_date: str = '2016-01-01'
    end_date: str = '2020-12-31'
    interval: str = '1d'
    action: bool = True
    rounding: bool = True

    df = StockDataLoader.get_download_df(
        target_ticker,
        start_date,
        end_date,
        interval,
        action,
        rounding
    )
    csv_name = '{ticker}_{start_date}_{end_date}_{interval}'.format(
        ticker = target_ticker,
        start_date = start_date,
        end_date = end_date,
        interval = interval
    )
    Util.save_pf_as_scv(df, csv_name, './data/raw/appl')

def download_nyt_archive():
    # data = NytDataLoader.get_archive_json(2019, 1)
    # print(data)
    NytDataLoader.save_archive_json_by_range(
        2016, 1,
        2020, 12
    )

# data loader functions
# download_apple_stock_history()
# download_nyt_archive()
