from london.commands.resource import ResourceCommand
from london.resource import Resource
from barbados.services.logging import LogService
import london.util
import requests
from time import sleep


class Ingredient(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/ingredients'
    path = './ingredients'

    def run(self):
        args = self._setup_args()
        self._validate_args(args)

        if args.action == 'create':
            self.create(args)
        elif args.action == 'delete':
            Resource.delete(self.endpoint, args)
        elif args.action == 'get':
            Resource.get(self.endpoint, args)
        else:
            Resource.delete(self.endpoint, args)
            self.create(args)

    def create(self, args):
        """
        This needs to be more reliable and do other things.
        :param args:
        :return:
        """
        if args.slug != 'all':
            Resource.create(self.endpoint, args, self.path)
            return

        LogService.info('Creating all ingredients')
        data = london.util.load_yaml_data_from_path(self.path)
        LogService.info("Found %i items." % len(data))
        success = 0
        retries = []
        for item in data:
            try:
                result = requests.post(self.endpoint, json=london.util.to_json(item))
                result.raise_for_status()
                success += 1
            except requests.exceptions.RequestException as e:
                # LogService.warning("Encountered error (%s). Will retry later." % e)
                retries.append(item)

        LogService.info("Succeeded with %i items." % success)
        LogService.info("Retrying with %i items. " % len(retries))

        for item in list(retries):
            try:
                result = requests.post(self.endpoint, json=london.util.to_json(item))
                result.raise_for_status()
                success += Resource._handle_error(result)
                retries.remove(item)
            except requests.exceptions.RequestException as e:
                LogService.error("Encountered error (%s). No more retries." % e)
                LogService.error(item)

        LogService.info("Succeeded with %i items." % success)

        # Refresh all indexes
        # There seems to be a problem where I hit ElasticSearch too quickly
        # and don't get all of the indexes in time. Manifested as 9 indexes
        # instead of 11.
        sleep(2)
        self._refresh_indexes()

    def _refresh_indexes(self):
        search_url = "%s/search" % self.endpoint

        parameters = {'kind': 'index'}

        search_results = requests.get(url=search_url, headers={}, params=parameters).json()
        LogService.info("Found %i indexes" % len(search_results))

        for result in search_results:
            slug = result.get('slug')
            refresh_endpoint = "%s/%s/refresh" % (self.endpoint, slug)
            LogService.info("Refreshing index %s" % slug)
            requests.post(refresh_endpoint)

        LogService.info("Refreshed all indexes!")
