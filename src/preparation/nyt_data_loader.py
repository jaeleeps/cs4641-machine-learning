import json
import os
from typing import Any, List

import requests
from typing_extensions import TypedDict

from src._model.nyt_archive_model import NytArchiveTransform_V1
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
            print(curr_year, '-', curr_month)
            # data_json: json = NytDataLoader.get_archive_json(curr_year, curr_month)
            # file_name: str = 'nyt_archive_{curr_year}-{curr_month}.json'.format(
            #     curr_year=curr_year,
            #     curr_month=curr_month if curr_month >= 10 else ('0{curr_month}'.format(curr_month=curr_month))
            # )
            # Util.save_json_as_json(
            #     data_json,
            #     file_name,
            #     './data/raw/nyt_archive'
            # )
            curr_month += 1
            if curr_month > 12:
                curr_month = 1
                curr_year += 1

    @staticmethod
    def transform_archive_json_by_range(
            raw_prefix: str,
            raw_dir_path: str,
            transformed_prefix: str,
            transformed_dir_path: str,
            start_year: int,
            start_month: int,
            end_year: int,
            end_month: int,
    ):
        curr_year: int = start_year
        curr_month: int = start_month
        while curr_year <= end_year and curr_month <= end_month:
            print(curr_year, '-', curr_month)
            raw_file_name: str = '{prefix}{curr_year}-{curr_month}.json'.format(
                prefix=raw_prefix,
                curr_year=curr_year,
                curr_month=curr_month if curr_month > 9 else '0{curr_month}'.format(
                    curr_month=curr_month
                )
            )
            path: str = os.path.join(raw_dir_path, raw_file_name)
            json_dict: dict = Util.get_json_dict_by_path(path)

            transformed_json: json = NytDataLoader.get_transformed_json(json_dict)
            transformed_file_name: str = '{prefix}{curr_year}-{curr_month}.json'.format(
                prefix=transformed_prefix,
                curr_year=curr_year,
                curr_month=curr_month if curr_month > 9 else '0{curr_month}'.format(
                    curr_month=curr_month
                )
            )
            Util.save_json_as_json(transformed_json, transformed_file_name, transformed_dir_path)

            curr_month += 1
            if curr_month > 12:
                curr_month = 1
                curr_year += 1

    @staticmethod
    def get_transformed_json(raw_json_dict: dict):
        json_dict: TypedDict('IRawNytArchive', {
            'copyright': str,
            'response': TypedDict('IRawNytArchive_Response')
        }) = raw_json_dict
        response: TypedDict('IRawNytArchive_Response', {
            'docs': List[dict],
            'meta': Any
        }) = json_dict['response']

        date_transformed_list_dict: dict = {}

        docs = response['docs']
        doc: dict
        for doc in docs:
            transform_v1: NytArchiveTransform_V1 = NytDataLoader.get_transformed_v1(doc)
            if not transform_v1:
                raise Exception('ERR')
            # 2019-01-01T00:00:03+0000 => 2019-01-01
            pub_date_key: str = transform_v1.pub_date[:10]
            if pub_date_key not in date_transformed_list_dict:
                date_transformed_list_dict[pub_date_key] = []
            date_transformed_list_dict[pub_date_key].append(transform_v1.dict())

        result_json: json = json.dumps(date_transformed_list_dict,
                                       indent=2,
                                       )
        return result_json

    @staticmethod
    def get_transformed_v1(doc: dict) -> NytArchiveTransform_V1:
        try:
            return NytArchiveTransform_V1(
                abstract=doc['abstract'],
                snippet=doc['snippet'],
                lead_paragraph=doc['lead_paragraph'],
                source=doc['source'],
                headline_main=doc['headline']['main'],
                pub_date=doc['pub_date'],
            )
        except Exception as e:
            print(e)
            return None
