import requests
from .baseimporter import BaseImporter
from barbados.services.logging import Log
from barbados.objects.ingredient import Ingredient
from barbados.serializers import ObjectSerializer


class IngredientImporter(BaseImporter):
    kind = 'ingredients'

    def import_(self, filepath, baseurl):
        data = IngredientImporter._fetch_data_from_path(filepath)

        Log.info("Starting import")

        endpoint = "%s/api/v1/ingredients/" % baseurl

        retries = []

        self.delete(endpoint)

        for ingredient in data:
            i = Ingredient(**ingredient)
            try:
                Log.info("Attempting %s" % i.slug)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(i, 'dict'))
                Log.info("Successful %s" % i.slug)
            except requests.HTTPError as e:
                Log.warning("Failed %s: %s, attempting retry." % (i.slug, e))
                retries.append(i)

        Log.info("Starting phase 2 with %i items" % len(retries))
        for i in retries:
            try:
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(i, 'dict'))
            except requests.HTTPError as e:
                Log.error("Failed %s: %s" % (i.slug, e))