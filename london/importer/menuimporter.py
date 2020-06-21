from .baseimporter import BaseImporter
from barbados.services.logging import Log
from barbados.factories import MenuFactory
from barbados.models import MenuModel
from barbados.serializers import ObjectSerializer
from barbados.indexers import indexer_factory
from barbados.validators import ObjectValidator
from barbados.indexes import index_factory, MenuIndex
from barbados.caches import MenuScanCache


class MenuImporter(BaseImporter):
    kind = 'menus'
    model = MenuModel

    def import_(self, filepath):
        data = MenuImporter._fetch_data_from_path(filepath)

        # Delete old data
        self.delete()

        Log.info("Starting import")
        for menu in data:
            m = MenuFactory.raw_to_obj(menu)
            db_obj = MenuModel(**ObjectSerializer.serialize(m, 'dict'))

            # Test for existing
            with self.pgconn.get_session() as session:
                session.add(db_obj)
                indexer_factory.get_indexer(m).index(m)

        # Validate
        self.validate()

        # Clear Cache and Index
        MenuScanCache.invalidate()

    def delete(self):
        Log.debug("Deleting old data from database")
        with self.pgconn.get_session() as session:
            deleted = session.query(self.model).delete()

        Log.info("Deleted %s" % deleted)
        index_factory.rebuild(MenuIndex)

    def validate(self):
        Log.info("Validating")
        with self.pgconn.get_session() as session:
            objects = session.query(self.model).all()
            for db_obj in objects:
                ObjectValidator.validate(db_obj, session=session, fatal=False)
