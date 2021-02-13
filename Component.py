# each basic component will have the following attributes
class Component:
    type = None
    name = None
    ports = []
    dependencies = []
    value = None
    def printInfo(self):
        print(self.name, *self.ports, *self.dependencies, self.value)
    def __init__(self, _type = None, _name = None, _ports = [], _dependencies = [], _value = None):
        self.type = _type
        self.name = _name
        self.ports = _ports
        self.dependencies = _dependencies
        self.value = _value