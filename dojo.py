''' varibles
 1.rooms- total number of rooms
  2.persons- total number of persons
  3.unlocated-total number of persons with no room
  4.located-total number of persons with rooms
  setup
  0.import the from classes Room and  person
  1 set up a list of this variables in the constructor
  2.create_room(room_name,room_type,max_num_of_occupants)
  '''
from room import Office
from room import Living
from persons import Staff
from persons import Fellow
import random


class Dojo(object):
    def __init__(self):
        self.rooms = []
        self.offices = []
        self.living_space = []
        self.persons_total = []
        self.persons_staff = []
        self.persons_fellow = []
        self.unllocated = []
        self.allocated = []

    def create_room(self, room_name, room_type):
        if room_type == "office" or room_type == "living space":
            for room_name in room_name:
                if not room_name in [room for room in self.rooms]:
                    if room_type == "office":
                        new_room = Office(room_name)
                        self.offices.append(new_room)
                        self.rooms.append(new_room)
                        print("an office called " + room_name + " has been created" )

                    elif room_type == 'living space':
                        new_room = Living(room_name)
                        self.living_space.append(new_room)
                        self.rooms.append(new_room)
                        print("a living space called " + room_name + "has been created")
                else:
                    print("room is already existing")


        else:
            return "invalid room type only office and living space allowed"

    def add_persons(self, person_name, person_role, person_accomodation='N'):
        if person_role == "FELLOW" or person_role == "STAFF":
            if person_role == "FELLOW":
                new_person=Fellow(person_name=person_name,person_accomodation=person_accomodation)
                self.persons_total.append(new_person)
                self.persons_fellow.append(new_person)
                self.room_assignment(new_person, person_accomodation=person_accomodation)

            if person_role == "STAFF":
                new_person = Staff(person_name=person_name)
                self.persons_total.append(new_person)
                self.persons_staff.append(new_person)
                self.room_assignment(new_person, person_accomodation=person_accomodation)
        else:
            return "No such role in this organisation"

    def room_assignment(self, person, person_accomodation):
        room_random = random.choice(self.offices)
        if len(room_random.room_occupants) >= room_random.room_size:
            return "this room is full"

        if len(room_random.room_occupants) < room_random.room_size and person.role == "STAFF":
            if person_accomodation == "Y":
                print("{} has been added to the office {} ".format(person.person_name, room_random.room_name))
                room_random.room_occupants.append(person)
                print("Staffs are not allowed living space")
            elif person_accomodation == "N":
                print("{} has been added to the office {} ".format(person.person_name, room_random.room_name))
                room_random.room_occupants.append(person)

        if len(room_random.room_occupants) <= room_random.room_size and person.role == "FELLOW":
            print("{} has been added to the office {} ".format(person.person_name, room_random.room_name))
            room_random.room_occupants.append(person)
            if person_accomodation == "Y":
                room_living = random.choice(self.living_space)
                if len(room_living.room_occupants) <= room_living.room_size:
                    print("{} has been added to the living room {} ".format(person.person_name, room_living.room_name))
                    room_living.room_occupants.append(person)

            elif person_accomodation == "N":
                print("{} has been added to the room {} ".format(person.person_name, room_random.room_name))
                room_random.room_occupants.append(person)