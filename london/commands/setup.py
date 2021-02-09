import argparse
import sys
import requests
import requests.exceptions
import london.util
import json


class Setup:

    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        endpoint = "http://localhost:8080/api/v1/setup"

        result = requests.get(endpoint)
        result.raise_for_status()
        print("Success!")

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Initiate setup',
                                         usage='amari setup')
        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
