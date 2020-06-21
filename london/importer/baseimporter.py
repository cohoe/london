import os
import time
import london.util
import requests
from barbados.services.logging import Log


class BaseImporter:

    def __init__(self):
        pass

    @staticmethod
    def import_(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def _fetch_data_from_path(filepath):
        if os.path.isfile(filepath):
            return london.util.read_yaml_file(filepath)
        else:
            return london.util.load_yaml_data_from_path(filepath)

    @staticmethod
    def post(endpoint, data):
        headers = {}
        response = requests.post(url=endpoint, json=data, headers=headers)

        if response.status_code != 200:
            raise requests.HTTPError(response.text)
