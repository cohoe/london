import london.util
import requests


class Resource:
    @staticmethod
    def get(endpoint, args):
        if args.slug == 'all':
            result = requests.get(endpoint)
        else:
            result = requests.get("%s/%s" % (endpoint, args.slug))
        print(result.json())
        return Resource._handle_error(result)

    @staticmethod
    def create(endpoint, args, path):
        data = london.util.load_yaml_data_from_path(path)
        for item in data:
            if item.get('slug') == args.slug or args.slug == 'all':
                print(item)
                result = requests.post(endpoint, json=item)

        return Resource._handle_error(result)

    @staticmethod
    def delete(endpoint, args):
        if args.slug == 'all':
            result = requests.delete(endpoint)
        else:
            result = requests.delete("%s/%s" % (endpoint, args.slug))
        return Resource._handle_error(result)

    @staticmethod
    def _handle_error(result):
        try:
            result.raise_for_status()
            print("Success!")
        except requests.exceptions.RequestException as e:
            print(result.text)
            print(result.status_code)
        return result
