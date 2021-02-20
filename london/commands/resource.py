import argparse
import sys
from london.resource import Resource


class ResourceCommand:
    @property
    def endpoint(self):
        raise NotImplementedError

    @property
    def path(self):
        raise NotImplementedError

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        if args.action == 'create':
            Resource.create(self.endpoint, args, self.path)
        elif args.action == 'delete':
            Resource.delete(self.endpoint, args)
        elif args.action == 'get':
            Resource.get(self.endpoint, args)
        else:
            Resource.delete(self.endpoint, args)
            Resource.create(self.endpoint, args, self.path)

    @staticmethod
    def _setup_args():
        parser = argparse.ArgumentParser(description='Manipulate a resource',
                                         usage='amari <resource> <action> <slug>')
        parser.add_argument('action', help='action', choices=['create', 'delete', 'recreate', 'get'])
        parser.add_argument('slug', help='slug')

        return parser.parse_args(sys.argv[2:])

    @staticmethod
    def _validate_args(args):
        pass
