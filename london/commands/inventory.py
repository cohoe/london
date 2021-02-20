from london.commands.resource import ResourceCommand


class Inventory(ResourceCommand):
    endpoint = 'http://localhost:8080/api/v1/inventories'
    path = './inventories'
