import json

import pandas as pd

import os
import sys


class Util:

    @staticmethod
    def save_pf_as_scv(
            data_df: pd.DataFrame,
            csv_file_name: str,
            relative_path: str
    ):
        script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
        proj_root_path = os.path.join(script_dir, '../')
        csv_path = os.path.join(proj_root_path, relative_path)
        data_df.to_csv(os.path.join(csv_path, csv_file_name))

    @staticmethod
    def save_json_as_json(
            data_json: json,
            json_file_name: str,
            relative_path: str
    ):
        script_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
        proj_root_path = os.path.join(script_dir, '../')
        json_path = os.path.join(proj_root_path, relative_path)
        target_path = os.path.join(json_path, json_file_name)
        with open(target_path, "w") as json_file:
            json.dump(data_json, json_file)
