from london.commands.resource import ResourceCommand


class Construction(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/constructions'
    path = './constructions'
