from .baseimporter import BaseImporter
from barbados.services.logging import LogService
from barbados.factories.list import ListFactory
from barbados.models.list import ListModel
from barbados.serializers import ObjectSerializer
from requests.exceptions import HTTPError


class DrinkListImporter(BaseImporter):
    kind = 'drinklists'
    model = ListModel

    def import_(self, filepath, baseurl, delete):
        data = DrinkListImporter._fetch_data_from_path(filepath)

        LogService.info("Starting import")
        endpoint = "%s/api/v1/lists" % baseurl

        if delete:
            self.delete(endpoint)

        for drinklist in data:
            m = ListFactory.raw_to_obj(drinklist)

            try:
                LogService.info("Attempting %s" % m.id)
                self.post(endpoint=endpoint, data=ObjectSerializer.serialize(m, 'dict'))
                LogService.info("Successful %s" % m.id)
            except HTTPError as e:
                LogService.warning("Failed %s: %s, attempting retry." % (m.id, e))
