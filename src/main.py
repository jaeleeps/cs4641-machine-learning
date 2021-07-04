from preparation.stock_data_loader import StockDataLoader

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
    StockDataLoader.save_pf_as_scv(df, csv_name, './data/raw')

# data loader functions
# download_apple_stock_history()
