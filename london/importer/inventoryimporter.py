from .baseimporter import BaseImporter
from barbados.services.logging import LogService
from barbados.factories.inventory import InventoryFactory
from barbados.models.inventory import InventoryModel
from barbados.serializers import ObjectSerializer
from requests.exceptions import HTTPError


class InventoryImporter(BaseImporter):
    kind = 'inventory'
    model = InventoryModel
    factory = InventoryFactory

    def import_(self, filepath, baseurl, delete):
        data = self._fetch_data_from_path(filepath)

        LogService.info("Starting import")
        endpoint = "%s/api/v1/inventories" % baseurl

        if delete:
            self.delete(endpoint)

        for item in data:
            m = self.factory.raw_to_obj(item)

            try:
                LogService.info("Attempting %s" % filepath)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(m, 'dict'))
                LogService.info("Successful %s" % filepath)
            except HTTPError as e:
                LogService.warning("Failed %s: %s, attempting retry." % (filepath, e))
