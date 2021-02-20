from london.commands.resource import ResourceCommand


class Glassware(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/glassware'
    path = './glassware'
