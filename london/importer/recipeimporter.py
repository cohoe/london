from requests import HTTPError
from .baseimporter import BaseImporter
from barbados.text import Slug
from barbados.factories import CocktailFactory
from barbados.services.logging import Log
from barbados.serializers import ObjectSerializer
from barbados.exceptions import ValidationException


class RecipeImporter(BaseImporter):
    kind = 'recipes'

    def import_(self, filepath, baseurl, delete):
        data = RecipeImporter._fetch_data_from_path(filepath)

        Log.info('Starting import')
        endpoint = "%s/api/v1/cocktails/" % baseurl

        if delete:
            self.delete(endpoint)

        problems = []

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
            except ValidationException as e:
                Log.error("Recipe failed validation")
                Log.error(cocktail)
                Log.error(e)
                problems.append({'slug': slug, 'error': e})
                continue

            try:
                Log.info("Attempting %s" % c.slug)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(c, 'dict'))
                Log.info("Successful %s" % c.slug)
            except HTTPError as e:
                Log.warning("Failed %s: %s, attempting retry." % (c.slug, e))
                problems.append({'slug': c.slug, 'error': e})

        print('Problems:')
        [print(p.get('slug'), p.get('error')) for p in problems]

        exit(len(problems))