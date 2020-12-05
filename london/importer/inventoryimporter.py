from .baseimporter import BaseImporter
from barbados.services.logging import Log
from barbados.factories.inventoryfactory import InventoryFactory
from barbados.models import InventoryModel
from barbados.serializers import ObjectSerializer
from requests.exceptions import HTTPError


class InventoryImporter(BaseImporter):
    kind = 'inventory'
    model = InventoryModel
    factory = InventoryFactory

    def import_(self, filepath, baseurl):
        data = self._fetch_data_from_path(filepath)

        Log.info("Starting import")
        endpoint = "%s/api/v1/inventories/" % baseurl

        self.delete(endpoint)

        for item in data:
            m = self.factory.raw_to_obj(item)

            try:
                Log.info("Attempting %s" % filepath)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(m, 'dict'))
                Log.info("Successful %s" % filepath)
            except HTTPError as e:
                Log.warning("Failed %s: %s, attempting retry." % (filepath, e))
