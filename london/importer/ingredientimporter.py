import requests
from london.importer.baseimporter import BaseImporter
from barbados.services.logging import LogService
from barbados.objects.ingredient import Ingredient
from barbados.serializers import ObjectSerializer
from barbados.factories.ingredientfactory import IngredientFactory


class IngredientImporter(BaseImporter):
    kind = 'ingredients'

    def import_(self, filepath, baseurl, delete):
        data = IngredientImporter._fetch_data_from_path(filepath)

        LogService.info("Starting import")

        endpoint = "%s/api/v1/ingredients/" % baseurl

        retries = []
        counts = {
            'success': 0,
            'fail': 0
        }

        if delete:
            self.delete(endpoint)

        for ingredient in data:
            # i = Ingredient(**ingredient)
            i = IngredientFactory.raw_to_obj(ingredient)
            try:
                self._perform_post(endpoint, i)
                counts['success'] += 1
            except requests.HTTPError as e:
                LogService.warning("Failed %s: %s, attempting retry." % (i.slug, e))
                retries.append(i)

        LogService.info("Starting phase 2 with %i items" % len(retries))
        for i in retries:
            try:
                self._perform_post(endpoint, i)
                counts['success'] += 1
            except requests.HTTPError as e:
                LogService.error("Failed %s: %s" % (i.slug, e))
                counts['fail'] += 1

        LogService.info("Found %i items to add." % len(data))
        LogService.info("Successfully added %i to the database." % counts['success'])
        LogService.info("Failed to add %i to the database." % counts['fail'])

        # Refresh all indexes
        self._refresh_indexes(endpoint=endpoint)

    def _refresh_indexes(self, endpoint):
        # @TODO need a sane library to make URLs without double slashes.
        search_url = endpoint + 'search'

        parameters = {'kind': 'index'}

        search_results = self.get(search_url, parameters)
        LogService.info("Found %i indexes" % len(search_results))

        for result in search_results:
            slug = result.get('slug')
            refresh_endpoint = "%s%s/refresh" % (endpoint, slug)
            LogService.info("Refreshing index %s" % slug)
            self.post(refresh_endpoint)

        LogService.info("Refreshed all indexes!")

    def _perform_post(self, endpoint, i):
        LogService.info("Attempting %s" % i.slug)
        self.post(endpoint=endpoint, data=ObjectSerializer.serialize(i, 'dict'))
        LogService.info("Successful %s" % i.slug)
