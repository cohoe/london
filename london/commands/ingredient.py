import argparse
import sys
import requests
import requests.exceptions
import london.util
import json


class Ingredient:

    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        endpoint = "http://localhost:8080/api/v1/ingredients/"

        if args.action == 'create':
            self._create(endpoint, args)
        elif args.action == 'delete':
            self._delete(endpoint, args)
        else:
            self._delete(endpoint, args)
            self._create(endpoint, args)

    def _create(self, endpoint, args):
        data = london.util.load_yaml_data_from_path('./ingredients')
        for item in data:
            if item.get('slug') == args.slug:
                print(item)
                result = requests.post(endpoint, json=item)

        return self._handle_error(result)

    def _delete(self, endpoint, args):
        result = requests.delete("%s%s" % (endpoint, args.slug))
        return self._handle_error(result)

    def _handle_error(self, result):
        try:
            result.raise_for_status()
            print("Success!")
        except requests.exceptions.RequestException as e:
            print(result.text)
            print(result.status_code)
        return result

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Manipulate ingredients',
                                         usage='amari ingredient <action> <slug>')
        parser.add_argument('action', help='action', choices=['create', 'delete', 'recreate'])
        parser.add_argument('slug', help='slug')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
