from requests import HTTPError
from .baseimporter import BaseImporter
from barbados.text import Slug
from barbados.factories import CocktailFactory
from barbados.services.logging import Log
from barbados.serializers import ObjectSerializer


class RecipeImporter(BaseImporter):
    kind = 'recipes'

    def import_(self, filepath):
        data = RecipeImporter._fetch_data_from_path(filepath)

        Log.info('Starting import')
        # endpoint = "https://jamaica-amari.cs.house/api/v1/cocktails/"
        endpoint = "http://localhost:8080/api/v1/cocktails/"

        for cocktail in data:
            try:
                slug = Slug(cocktail['display_name'])
                Log.info("Working %s" % slug)
                c = CocktailFactory.raw_to_obj(cocktail, slug)
            except KeyError as e:
                Log.error("Something has bad data!")
                Log.error(cocktail)
                Log.error(e)
                continue

            try:
                Log.info("Attempting %s" % c.slug)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(c, 'dict'))
                Log.info("Successful %s" % c.slug)
            except HTTPError as e:
                Log.warning("Failed %s: %s, attempting retry." % (c.slug, e))