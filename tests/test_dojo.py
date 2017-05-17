import unittest
from dojo import Dojo


class TestRoomCreation(unittest.TestCase):

    """ Test cases for successful room creation and successful person addition
       """
    def setUp(self):
        self.dojo = Dojo()

    def test_create_room(self):
        self.assertEqual(len(self.dojo.rooms), 0)

    def test_invalid_room(self):
        self.dojo.create_room("kenya", "kenya")
        self.assertEqual(len(self.dojo.rooms), 0)

    def test_create_office(self):
        self.dojo.create_room("office", ["blue"])
        self.assertEqual(len(self.dojo.offices), 1)

    def test_create_living_space(self):
        self.dojo.create_room("living", ["green"])
        self.assertEqual(len(self.dojo.living_space), 1)

    def test_create_multiple_offices(self):
        self.dojo.create_room('office', ["green", "blue"])
        self.assertEqual(len(self.dojo.offices), 2)

    def test_add_persons_invalid_role(self):
        self.dojo.create_room("office", ["blue"])
        self.dojo.add_persons("Farhan Abdi", 'jobless', "N")
        self.assertEqual(len(self.dojo.persons_total), 0)

    def test_add_persons_Fellow(self):
        self.dojo.create_room(["blue"], "office")
        self.dojo.create_room(["blue"], "living space")
        self.dojo.add_persons("Farhan Abdi", 'FELLOW', 'Y')
        self.assertEqual(len(self.dojo.persons_fellow), 1)

    def test_add_persons_staff(self):
        self.dojo.create_room(["blue"], "office")
        self.dojo.create_room(["blue"], "living space")
        self.dojo.add_persons("Farhan Abdi", "STAFF", "N")
        self.assertEqual(len(self.dojo.persons_staff), 1)

    def test_add_persons_staff_to_offices(self):
        self.dojo.create_room( "office", ['blue'])
        self.dojo.add_persons("farhan", "STAFF", "Y")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(len(self.dojo.living_space), 0)

    def test_add_persons_fellow_to_offices_and_living_spaces(self):
        self.dojo.create_room("office", ['blue'])
        self.dojo.create_room("living", ['green'])
        self.dojo.add_persons("farhan", "FELLOW", "Y")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(len(self.dojo.living_space), 1)
        self.dojo.add_persons("farhan", "FELLOW", "N")
        self.assertEqual(len(self.dojo.offices), 1)
        self.assertEqual(len(self.dojo.living_space), 1)

    def test_duplicate_room_names(self):
        self.dojo.create_room("office", ["blue"])
        self.dojo.create_room("office", ["blue"])
        self.assertEqual(len(self.dojo.offices), 1)
