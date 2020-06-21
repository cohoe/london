from .baseimporter import BaseImporter
from barbados.services.logging import Log
from barbados.factories import MenuFactory
from barbados.models import MenuModel
from barbados.serializers import ObjectSerializer
from requests.exceptions import HTTPError


class MenuImporter(BaseImporter):
    kind = 'menus'
    model = MenuModel

    def import_(self, filepath, baseurl):
        data = MenuImporter._fetch_data_from_path(filepath)

        Log.info("Starting import")
        endpoint = "%s/api/v1/menus/" % baseurl

        self.delete(endpoint)

        for menu in data:
            m = MenuFactory.raw_to_obj(menu)

            try:
                Log.info("Attempting %s" % m.slug)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(m, 'dict'))
                Log.info("Successful %s" % m.slug)
            except HTTPError as e:
                Log.warning("Failed %s: %s, attempting retry." % (m.slug, e))
