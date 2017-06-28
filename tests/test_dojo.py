import unittest
from dojo import Dojo
from tests import testdb
import sys
import os
from models.persons import Staff


class TestRoomCreation(unittest.TestCase):

    """ Test cases for successful room creation and successful person addition
       """
    def setUp(self):
        self.dojo = Dojo()
        self.file = open("allocate.txt", "w+")


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
        self.dojo.add_persons("Farhan Abdi", 'ljjlll', "N")
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
        self.dojo.create_room("office", ['blue'])
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

    def test_print_rooms(self):
        self.dojo.create_room("office", ["blue"])
        self.dojo.add_persons("eldi", "STAFF", "N")
        self.dojo.print_room("blue")
        value = sys.stdout
        output = value.getvalue()
        self.assertIn('eldi', output)

    def test_print_allocations_on_screen(self):
        self.dojo.create_room("office", ["blue"])
        self.dojo.add_persons("eldi", "STAFF", "N")
        self.dojo.print_allocations()
        value = sys.stdout
        output = value.getvalue()
        self.assertIn('eldi', output)

    def test_print_allocations_to_file(self):
        self.dojo.create_room("office", ["grey"])
        self.dojo.create_room("living", ["red"])
        self.dojo.add_persons("farhan", "FELLOW", "Y")
        self.dojo.print_allocations("allocate.txt")
        content_on_file = self.file.readlines()
        first_room = content_on_file[1]
        self.assertEqual(str(first_room), "grey\n")

    def test_print_unallocated_to_screen(self):
        self.dojo.create_room("office", ["grey"])
        self.dojo.create_room("living", ["red"])
        self.dojo.add_persons("farhan", "FELLOW", "Y")
        self.dojo.add_persons("peter", "FELLOW", "Y")
        self.dojo.add_persons("Merge", "FELLOW", "Y")
        self.dojo.add_persons("Dom", "FELLOW", "Y")
        self.dojo.add_persons("Benja", "FELLOW", "Y")
        self.dojo.add_persons("Bryan", "FELLOW", "Y")
        self.dojo.add_persons("Rash", "FELLOW", "Y")
        self.dojo.add_persons("Rash", "FELLOW", "Y")
        self.assertEqual(len(self.dojo.unallocated), 2)

    def test_successful_save_state_creates_database(self):
        self.assertTrue(os.path.isfile("/Users/farhanabdi/dojo-room-allocation/models/dojo.db"))

    def test_save_state_succesfully_stores_data_in_database(self):
        self.dojo.create_room("office", ["grey"])
        self.dojo.add_persons("farhan", "FELLOW", "Y")
        room = testdb.Rooms(room_name="red", room_type="office")
        testdb.s.add(room)
        testdb.s.commit()
        person = testdb.Persons(person_name="test", person_type="staff", person_accomodation="N",
                                 room_name="red", room_type="office", rooms=room)
        testdb.s.add(person)
        testdb.s.commit()
        person_db=testdb.s.query(testdb.Persons).all()
        self.assertEqual(len(person_db), 1)

    def test_load_state_load_people(self):
        list_people = testdb.s.query(testdb.Persons).all()
        for person in list_people:
            person_name = person.person_name
            prs = Staff(person_name)
            self.dojo.persons_total.append(prs)
            self.assertEqual(len(self.dojo.persons_total), 1)
            os.remove("test.db")

    def tearDown(self):
        self.file.close()
        os.remove("allocate.txt")






