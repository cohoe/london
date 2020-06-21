import argparse
import sys
from london.importer import Importer


class Import:

    def __init__(self):
        pass

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        Importer.get_importer(args.object).import_(args.filepath)

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Import something to the API',
                                         usage='london import <object> <recipepath>')
        parser.add_argument('object', help='object to import', choices=Importer.supported_importers())
        parser.add_argument('filepath', help='path to the yaml file (or directory) containing the objects')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
