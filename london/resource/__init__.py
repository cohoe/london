import london.util
import requests
from barbados.services.logging import LogService


class Resource:
    @staticmethod
    def get(endpoint, args):
        LogService.info("Getting %s" % args.slug)
        if args.slug == 'all':
            result = requests.get(endpoint)
        else:
            result = requests.get("%s/%s" % (endpoint, args.slug))
        # print(result.json())
        Resource._handle_error(result)

    @staticmethod
    def create(endpoint, args, path):
        LogService.info("Creating %s" % args.slug)
        data = london.util.load_yaml_data_from_path(path)
        LogService.info("Found %i items." % len(data))
        success = 0
        for item in data:
            if item.get('slug') == args.slug or args.slug == 'all':
                # print(item)
                result = requests.post(endpoint, json=london.util.to_json(item))
                success += Resource._handle_error(result)
        LogService.info("Succeeded with %i items." % success)

    @staticmethod
    def delete(endpoint, args):
        LogService.info("Deleting %s" % args.slug)
        if args.slug == 'all':
            result = requests.delete(endpoint)
        else:
            result = requests.delete("%s/%s" % (endpoint, args.slug))

        Resource._handle_error(result)

    @staticmethod
    def _handle_error(result):
        """
        Parse an HTTP request for success/failure. Return a count of the success.
        :param result:
        :return: Integer count of success (THIS IS NOT A RETURN CODE!)
        """
        try:
            result.raise_for_status()
            LogService.debug('Success!')
            return 1
        except requests.exceptions.RequestException as e:
            LogService.error("Error handling URL: %i" % result.status_code)
            LogService.error(result.request.body)
            LogService.error(result.json().get('message'))
            return 0
