from requests import HTTPError
from .baseimporter import BaseImporter
from barbados.objects.text import Slug
from barbados.factories.construction import ConstructionFactory
from barbados.services.logging import LogService
from barbados.serializers import ObjectSerializer
from barbados.exceptions import ValidationException


class ConstructionImporter(BaseImporter):
    kind = 'constructions'

    def import_(self, filepath, baseurl, delete):
        data = ConstructionImporter._fetch_data_from_path(filepath)

        LogService.info('Starting import')
        endpoint = "%s/api/v1/constructions" % baseurl

        if delete:
            self.delete(endpoint)

        problems = []
        count = 0

        for item in data:
            slug = item['slug']
            try:
                LogService.info("Working %s" % slug)
                c = ConstructionFactory.raw_to_obj(item)
            except KeyError as e:
                LogService.error("Something has bad data!")
                LogService.error(item)
                LogService.error(e)
                problems.append({'slug': slug, 'error': e})
                continue
            except ValidationException as e:
                LogService.error("Construction failed validation")
                LogService.error(item)
                LogService.error(e)
                problems.append({'slug': slug, 'error': e})
                continue

            try:
                LogService.info("Attempting %s" % c.slug)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(c, 'dict'))
                count += 1
                LogService.info("Successful %s" % c.slug)
            except HTTPError as e:
                LogService.warning("Failed %s: %s, attempting retry." % (c.slug, e))
                problems.append({'slug': c.slug, 'error': e})

        print("Success count: %i" % count)
        print("Problems count: %i" % len(problems))

        [print(p.get('slug'), p.get('error')) for p in problems]

        exit(len(problems))
