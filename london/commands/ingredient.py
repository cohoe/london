from london.commands.resource import ResourceCommand


class Ingredient(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/ingredients'
    path = './ingredients'

    # @TODO takes two passes and doesnt re-index