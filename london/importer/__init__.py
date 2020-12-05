from .ingredientimporter import IngredientImporter
from .menuimporter import MenuImporter
from .recipeimporter import RecipeImporter
from .inventoryimporter import InventoryImporter


class Importer:
    importers = {}

    @classmethod
    def register_importer(cls, importer_class):
        cls.importers[importer_class.kind] = importer_class

    @classmethod
    def get_importer(cls, kind):
        return cls.importers[kind]()

    @classmethod
    def supported_importers(cls):
        return cls.importers.keys()


Importer.register_importer(IngredientImporter)
Importer.register_importer(MenuImporter)
Importer.register_importer(RecipeImporter)
Importer.register_importer(InventoryImporter)
