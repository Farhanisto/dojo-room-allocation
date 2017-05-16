import unittest
from dojo import Dojo


class TestRoomCreation(unittest.TestCase):

    """ Test cases to for successful and failed room creation 
          1.create create room
          2.roomss created are nothing other than offices or living quters
          3can create office
          4. can create multiple offices
          5.can can create living quter 
          6.can create multiple living quters
       """

    def test_create_room(self):
        self.dojo = Dojo()
        self.assertEqual(len(self.dojo.rooms), 0)

    def test_invalid_room(self):
        self.dojo = Dojo()
        self.assertEqual(self.dojo.create_room("kenya", "kenya"),
                         "invalid room type only office and living space allowed")

    def test_create_office(self):
        self.dojo = Dojo()
        self.dojo.create_room(["blue"], "office")
        self.assertEqual(len(self.dojo.rooms), 1)

    def test_create_living_space(self):
        self.dojo = Dojo()
        self.dojo.create_room(["green"], "living space")
        self.assertEqual(len(self.dojo.living_space), 1)

    def test_create_multiple_offices(self):
        self.dojo = Dojo()
        self.dojo.create_room(["green", "blue"], 'office')
        self.assertEqual(len(self.dojo.offices), 2)

    def test_add_persons_invalid_role(self):
        self.dojo = Dojo()
        self.dojo.create_room(["blue"], "office")
        self.assertEqual(self.dojo.add_persons("Farhan Abdi", 'jobless'), "No such role in this organisation")

    def test_add_persons_Fellow(self):
        self.dojo = Dojo()
        self.dojo.create_room(["blue"], "office")
        self.dojo.create_room(["blue"], "living space")
        self.dojo.add_persons("Farhan Abdi", 'FELLOW', 'Y')
        self.assertEqual(len(self.dojo.persons_fellow), 1)


    def test_add_persons_staff(self):
        self.dojo = Dojo()
        self.dojo.create_room(["blue"], "office")
        self.dojo.create_room(["blue"], "living space")
        self.dojo.add_persons("Farhan Abdi", "STAFF", "N")
        self.assertEqual(len(self.dojo.persons_staff), 1)

    def test_add_persons_staff_to_offices(self):
        self.dojo = Dojo()
        self.dojo.create_room(['blue'], "office")
        self.dojo.add_persons("farhan", "STAFF", "Y")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(len(self.dojo.living_space), 0)

    def test_add_persons_fellow_to_offices_and_living_spaces(self):
        self.dojo = Dojo()
        self.dojo.create_room(['blue'], "office")
        self.dojo.create_room(['blue'], "living space")
        self.dojo.add_persons("farhan", "FELLOW", "Y")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(len(self.dojo.living_space), 1)
        self.dojo.add_persons("farhan", "FELLOW", "N")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(len(self.dojo.living_space), 1)





