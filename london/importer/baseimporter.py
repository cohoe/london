import os
import london.util
import requests
from barbados.services.logging import LogService


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
    def post(endpoint, data=None):
        headers = {}
        response = requests.post(url=endpoint, json=data, headers=headers)

        if response.status_code != 200:
            raise requests.HTTPError(response.text)

    @staticmethod
    def get(endpoint, parameters=None):
        if parameters is None:
            parameters = {}
        headers = {}
        response = requests.get(url=endpoint, headers=headers, params=parameters)

        if response.status_code != 200:
            raise requests.HTTPError(response.text)

        return response.json()

    @staticmethod
    def delete(endpoint):
        LogService.info("Performing DELETE against %s" % endpoint)
        response = requests.delete(url=endpoint)

        if response.status_code >= 400:
            raise requests.HTTPError(response.text)
