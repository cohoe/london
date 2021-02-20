from london.commands.resource import ResourceCommand


class Lists(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/lists'
    path = './lists'
