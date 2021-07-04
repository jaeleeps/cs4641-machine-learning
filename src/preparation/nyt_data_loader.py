import json

import requests

from src.env.config import Config
from src.preparation.uitl import Util


class NytDataLoader:

    @staticmethod
    def get_archive_json(
            year: int,
            month: int,
    ):
        URL: str = 'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?api-key={API_KEY}'.format(
            year=year,
            month=month,
            API_KEY=Config.NYT_DEVELOPER_API_KEY
        )
        res = requests.get(URL)
        status_code = res.status_code
        res.raise_for_status()
        return res.json()

    @staticmethod
    def save_archive_json_by_range(
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
    ):
        curr_year: int = start_year
        curr_month: int = start_month

        while curr_year <= end_year and curr_month <= end_month:
            data_json: json = NytDataLoader.get_archive_json(curr_year, curr_month)
            file_name: str = 'nyt_archive_{curr_year}-{curr_month}.json'.format(
                curr_year=curr_year,
                curr_month=curr_month if curr_month >= 10 else ('0{curr_month}'.format(curr_month=curr_month))
            )
            Util.save_json_as_json(
                data_json,
                file_name,
                './data/raw/nyt_archive'
            )
            curr_month += 1
            if curr_month > 12:
                curr_month = 1
                curr_year += 1
