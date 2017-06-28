
class Persons(object):
    """This is the persons class with the subclassess of the staff class and the fellow"""

    def __init__(self, person_name, role=None, person_accomodation="N"):
        self.person_name = person_name
        self.role = role
        self.person_accomodation = person_accomodation


class Staff(Persons):
    def __init__(self, person_name):
        super(Staff, self).__init__(person_name, role="STAFF", person_accomodation="N")


class Fellow(Persons):
    def __init__(self,person_name,person_accomodation):
        super(Fellow, self).__init__(person_name, role="FELLOW", person_accomodation=person_accomodation)

