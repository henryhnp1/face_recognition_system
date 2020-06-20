class Building(object):
    def __init__(self, pk, name, location, number_of_floor, acreage):
        super(Building,self).__init__()
        self.pk = pk
        self.name = name
        self.location = location
        self.number_of_floor = number_of_floor
        self.acreage = acreage


class TypeOfFloor(object):
    def __init__(self, pk, name, description):
        super(TypeOfFloor, self).__init__()
        self.pk = pk
        self.name = name
        self.description = description


class Permission(object):
    def __init__(self, pk, name, description):
        super(Permission, self).__init__()
        self.pk = pk
        self.name = name
        self.description = description

class Floor(object):
    def __init__(self, pk, name, building, type_of_floor, number_of_aparment):
        super(Building,self).__init__()
        self.pk = pk
        self.name = name
        self.building = building
        self.type_of_floor = type_of_floor
        self.number_of_aparment = number_of_aparment