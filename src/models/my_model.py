class Building(object):
    def __init__(self, pk, name, location, number_of_floor, acreage):
        # super(Building,self).__init__()
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
        super(Floor,self).__init__()
        self.pk = pk
        self.name = name
        self.building = building
        self.type_of_floor = type_of_floor
        self.number_of_aparment = number_of_aparment

class Door(object):
    def __init__(self, pk, name, floor, permission):
        self.pk = pk
        self.name = name
        self.floor = floor
        self.permission = permission

class RoleDoor(object):
    def __init__(self, pk, name, description):
        self.pk = pk
        self.name = name
        self.description = description

class Apartment(object):
    def __init__(self, pk, name, floor, status):
        self.pk = pk
        self.name = name
        self.floor = floor
        self.status = status

class Staff(object):
    def __init__(self, pk, company, office, name, birthday, gender, id_card, phone,village, current_accommodation):
        self.pk = pk
        self.company = company
        self.office = office
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.id_card = id_card
        self.phone = phone
        self.village = village
        self.current_accommodation = current_accommodation

class Company(object):
    def __init__(self, pk, name, phone, apartment, office=None):
        self.pk = pk
        self.name = name
        self.phone = phone
        self.apartment = apartment
        self.office = office

class Company_Office_Building(object):
    def __init__(self, pk, name, office_pk, office_name, floor_pk, floor_name, building_pk, building_name):
        self.pk = pk
        self.name = name
        self.office_pk = office_pk
        self.office_name = office_name
        self.floor_pk = floor_pk
        self.floor_name = floor_name
        self.building_pk = building_pk
        self.building_name = building_name

class Apartment_Floor_Building(object):
    def __init__(self, pk, name, floor_pk, floor_name, building_pk, building_name):
        self.pk = pk
        self.name = name
        self.floor_pk = floor_pk
        self.floor_name = floor_name
        self.building_pk = building_pk
        self.building_name = building_name

class Image_Person(object):
    def __init__(self, pk, owner, url, is_delete):
        self.pk = pk
        self.owner = owner
        self.url = url
        self.is_delete = is_delete

class ImageCapture:
    def __init__(self, index, owner, data):
        self.index = index
        self.owner = owner
        self.data = data

class PersonDraffInfo:
    def __init__(self, pk, name, birthday, id_card, phone, name_en):
        self.pk = pk
        self.name = name
        self.birthday = birthday
        self.id_card = id_card
        self.phone = phone
        self.name_en = name_en

class GuestVisit:
    def __init__(self, pk, name, birthday, gender, id_card, phone, village, accommodation, apartment, time_in, time_out, visit_to):
        self.pk = pk
        self.name = name
        self.birthday = birthday
        self.gender = gender
        self.id_card = id_card
        self.phone = phone
        self.village = village
        self.accommodation = accommodation
        self.apartment = apartment
        self.time_in = time_in
        self.time_out = time_out
        self.visit_to = visit_to