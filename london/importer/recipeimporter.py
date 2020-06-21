from .baseimporter import BaseImporter
from barbados.text import Slug
from barbados.factories import CocktailFactory
from barbados.services.logging import Log
from barbados.models import CocktailModel
from barbados.serializers import ObjectSerializer
from barbados.validators import ObjectValidator
from barbados.indexers import indexer_factory
from barbados.indexes import index_factory, RecipeIndex
from barbados.caches import CocktailScanCache


class RecipeImporter(BaseImporter):
    kind = 'recipe'

    def import_(self, filepath):
        dicts_to_import = RecipeImporter._fetch_data_from_path(filepath)

        if len(dicts_to_import) > 1:
            self.delete(delete_all=True)

        for cocktail_dict in dicts_to_import:
            try:
                slug = Slug(cocktail_dict['display_name'])
                Log.info("Working %s" % slug)
                c = CocktailFactory.raw_to_obj(cocktail_dict, slug)
            except KeyError as e:
                Log.error("Something has bad data!")
                Log.error(cocktail_dict)
                Log.error(e)
                continue

            self.delete(cocktail=c)

            db_obj = CocktailModel(**ObjectSerializer.serialize(c, 'dict'))
            with self.pgconn.get_session() as session:
                session.add(db_obj)
                Log.info("Successfully [re]created %s" % c.slug)

                ObjectValidator.validate(db_obj, session=session, fatal=False)

            indexer_factory.get_indexer(c).index(c)

        CocktailScanCache.invalidate()

    def delete(self, cocktail=None, delete_all=False):

        if cocktail:
            with self.pgconn.get_session() as session:
                existing = session.query(CocktailModel).get(cocktail.slug)

                if existing:
                    Log.debug("Deleting %s" % existing.slug)
                    deleted = session.delete(existing)
            return

        if delete_all is True:
            with self.pgconn.get_session() as session:
                Log.debug("Deleting all CocktailModel")
                deleted = session.query(CocktailModel).delete()
                Log.info("Deleted %s from %s" % (deleted, CocktailModel.__tablename__))
                index_factory.rebuild(RecipeIndex)
