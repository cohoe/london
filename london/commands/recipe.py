from london.commands.resource import ResourceCommand


class Recipe(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/cocktails'
    path = './recipes'
