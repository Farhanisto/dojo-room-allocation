
from room import Office
from room import Living
from persons import Staff
from persons import Fellow
import random
import os


class Dojo(object):
    """Program to create rooms and add people to the rooms in accordance to their roles"""

    def __init__(self):
        self.rooms = []
        self.offices = []
        self.living_space = []
        self.persons_total = []
        self.persons_staff = []
        self.persons_fellow = []
        self.unallocated_office = []
        self.unallocated_living_space = []
        self.unallocated = []
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
            print("you have not entered a  room name.")

    def add_persons(self, person_name, person_role, person_accomodation):
        if person_role == "FELLOW" or person_role == "STAFF":
            if person_role == "FELLOW":
                new_person = Fellow(person_name=person_name, person_accomodation=person_accomodation)
                self.persons_fellow.append(new_person)
                self.room_assignment(new_person, person_accomodation=person_accomodation)

            if person_role == "STAFF":
                new_person = Staff(person_name=person_name)
                self.persons_staff.append(new_person)
                self.room_assignment(new_person, person_accomodation=person_accomodation)
        else:
            return "No such role in this organisation"

    def room_assignment(self, person, person_accomodation):
        try:
            room_random = random.sample(self.offices, len(self.offices))
            for room_random in room_random:
                if len(room_random.room_occupants) >= room_random.room_size:
                    print("this room is full " + room_random.room_name)
                    self.unallocated.append(person)

                if len(room_random.room_occupants) <= room_random.room_size and person.role == "STAFF":
                    if person_accomodation == "Y":
                        print("{} has been added to the office {} ".format(person.person_name,
                                                                           room_random.room_name))
                        room_random.room_occupants.append(person)
                        self.allocated.append(room_random.room_occupants)
                        print("Staff are not allowed living space")
                    else:
                        person_accomodation == "N"
                        print("{} has been added to the office {} ".format(person.person_name,
                                                                           room_random.room_name))
                        room_random.room_occupants.append(person)
                if len(room_random.room_occupants) <= room_random.room_size and person.role == "FELLOW":

                    if person_accomodation == "Y":
                        print("{} has been added to the office{} ".format(person.person_name,
                                                                          room_random.room_name))
                        room_random.room_occupants.append(person)
                        room_living = random.choice(self.living_space)
                        if len(room_living.room_occupants) <= room_living.room_size:
                            print("{} has been added to the living room {} ".format(person.person_name,
                                                                                    room_living.room_name))
                            room_living.room_occupants.append(person)

                    if person_accomodation == "N":
                        print("{0} has been added to the office {1} ".format(person.person_name,
                                                                             room_random.room_name))
                        room_random.room_occupants.append(person)



        except IndexError:
            print("You have no rooms to start with , add rooms first")
            self.unallocated.append(person)

    def print_room(self, room_name):

        if room_name not in [room.room_name for room in self.rooms]:
            print("Sorry.That room does not exist.")
        else:
            for room_to_check in self.rooms:
                if room_name == room_to_check.room_name:
                    if len(room_to_check.room_occupants) > 0:
                        for occupant in room_to_check.room_occupants:
                            self.persons_total.append(occupant.person_name)
                        for name in self.persons_total:
                            print("{} ".format(str(name)))

                    else:
                        print("{0} space {1} contains no occupants".format(room_to_check.room_type,
                                                                           room_to_check.room_name))

    def print_allocations(self, filename=None):
        if not self.rooms:
            print("Sorry.No rooms exist. Please create one")
        else:
            if filename is None:
                for room in self.rooms:
                    if len(room.room_occupants) > 0:
                        self.allocated = [occupant.person_name for occupant in room.room_occupants]
                        str1 = ', '.join(str(e) for e in self.allocated)
                        print("\n"
                              "{0} \n".format(room.room_name),
                              "\n"
                              "------------------------------------------"
                              "\n"
                              "{0}".format(str1),
                              "\n"
                              )
                    else:
                        print("\n"
                              "{} \n".format(room.room_name),
                              "\n"
                              "------------------------------------------\n"
                              "\n"
                              "This {} has no occupants".format(room.room_type),
                              "\n"
                              )
            elif filename not in [file for file in os.listdir("/home/farhan/dojo-room-allocation")]:
                files = [file for file in os.listdir("/home/farhan/dojo-room-allocation")
                         if file.endswith(".txt") and not file.startswith("requirements")]
                if len(files) > 0:
                    print("You have already created a file for the system using it instead " + files[0])
                else:
                    print("creating file  " + filename + "for the system")
                    doc = open(filename, "a+")
                    for room in self.rooms:
                        if len(room.room_occupants) > 0:
                            self.allocated = [occupant.person_name for occupant in room.room_occupants]
                            str1 = ', '.join(str(e) for e in self.allocated)
                            doc.write("\n" + room.room_name +
                                  "\n" +
                                  "------------------------------------------"
                                  "\n"
                                  "{0}".format(str1) +
                                  "\n"
                                  )
                            doc.close()
                        else:
                            print("\n"
                                  "{} \n".format(room.room_name),
                                  "\n"
                                  "------------------------------------------\n"
                                  "\n"
                                  "This {} has no occupants".format(room.room_type),
                                  "\n"
                                  )
            else:
                print("append to" + filename)
                doc = open(filename, "a+")
                for room in self.rooms:
                    if len(room.room_occupants) > 0:
                        self.allocated = [occupant.person_name for occupant in room.room_occupants]
                        str1 = ', '.join(str(e) for e in self.allocated)
                        doc.write("\n" + room.room_name +
                                  "\n" +
                                  "------------------------------------------"
                                  "\n"
                                  "{0}".format(str1) +
                                  "\n"
                                  )
                        doc.close()

    def print_unallocated(self, filename=None):
        if filename is None:
            if not self.rooms:
                print("Sorry.No rooms exist. Please create one")
            else:
                for room in self.unallocated:
                    print(room.person_name)

        elif filename not in os.listdir("/home/farhan/dojo-room-allocation/unallocated"):
            doc = open(filename, "a+")
            for room in self.unallocated:
                doc.write(room.person_name)
                doc.close()
        else:
            doc = open(filename, "a+")
            for room in self.unallocated:
                doc.write(room.person_name)
                doc.close()


    def rellocate_people
