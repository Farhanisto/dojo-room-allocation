"""Program to create rooms and and people to the rooms in accordance to their roles"""

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
        self.unllocated_office = []
        self.unllocated_living_space = []
        self.unllocated=[]
        self.allocated = []

    def create_room(self, room_type, room_name):
        if isinstance(room_name, list):
            if room_type == "office" or room_type == "living":
                for room_name in room_name:
                    if room_name not in [room.room_name for room in self.rooms]:
                        if room_type == "office":
                            new_room = Office(room_name)
                            self.offices.append(new_room)
                            self.rooms.append(new_room)
                            print("an office called " + room_name + " has been created")

                        elif room_type == 'living':
                            new_room = Living(room_name)
                            self.living_space.append(new_room)
                            self.rooms.append(new_room)
                            print("a living space called " + room_name + "has been created")
                    else:
                        print("room is already existing")

            else:
                print("invalid room type only office and living space allowed")
        else:
            print("you have not entered a list as your  room name.")

    def add_persons(self, person_name, person_role, person_accomodation):
        if person_role == "FELLOW" or person_role == "STAFF":
            if person_role == "FELLOW":
                new_person = Fellow(person_name=person_name, person_accomodation=person_accomodation)
                self.persons_total.append(new_person)
                self.persons_fellow.append(new_person)
                self.room_assignment(new_person, person_accomodation=person_accomodation)

            if person_role == "STAFF":
                new_person = Staff(person_name=person_name)
                self.persons_total.append(new_person)
                self.persons_staff.append(new_person)
                self.room_assignment(new_person, person_accomodation=person_accomodation)
        else:
            print("No such role in this organisation")

    def room_assignment(self, person, person_accomodation):
        try:
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

            if len(room_random.room_occupants) <= room_random.room_size and person.role == "FELLOW" :

                if person_accomodation == "Y":
                    print("{} has been added to the office){} ".format(person.person_name, room_random.room_name))
                    room_random.room_occupants.append(person)
                    room_living = random.choice(self.living_space)
                    if len(room_living.room_occupants) <= room_living.room_size:
                        print("{} has been added to the living room {} ".format(person.person_name,
                                                                                room_living.room_name))
                        room_living.room_occupants.append(person)

                if person_accomodation == "N":
                    print("{} has been added to the office){} ".format(person.person_name, room_random.room_name))
                    room_random.room_occupants.append(person)

        except IndexError:
            print("You have no rooms to start with , add rooms first")





