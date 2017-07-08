import os
import random
import tkinter as tk
from shutil import copy
from tkinter import filedialog
import pickle

from models import db_room
from models.persons import Fellow
from models.persons import Staff
from models.room import Living
from models.room import Office


from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class Dojo(object):
    """Program to create rooms and add people to the rooms in accordance to their roles"""

    def __init__(self):
        self.rooms = []
        self.offices = []
        self.living_space = []
        self.persons_staff = []
        self.persons_fellow = []
        self.persons_total = []
        self.unallocated_office = []
        self.unallocated_living_space = []
        self.unallocated = []
        self.allocated = []

    def create_room(self, room_type, room_name):
        if isinstance(room_name, list) or isinstance(room_name, str):
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
            print("No such role in this organisation")

    def room_assignment(self, person, person_accomodation):

        try:
            room_random = random.choice(self.offices)
            if len(room_random.room_occupants) >= room_random.room_size:
                print("this room is full " + room_random.room_name)
                self.unallocated.append(person)
                self.unallocated_office.append(person)

            if len(room_random.room_occupants) < room_random.room_size and person.role == "STAFF":
                if person_accomodation == "Y":
                    print("{} has been added to the office {} ".format(person.person_name,
                                                                       room_random.room_name))
                    room_random.room_occupants.append(person)
                    self.persons_total.append(person)
                    print("Staff are not allowed living space")
                elif person_accomodation == "N":
                    print("{} has been added to the office {} ".format(person.person_name,
                                                                       room_random.room_name))
                    room_random.room_occupants.append(person)

            if len(room_random.room_occupants) <= room_random.room_size and person.role == "FELLOW":

                if person_accomodation == "Y":
                    print("{} has been added to the office{} ".format(person.person_name,
                                                                      room_random.room_name))
                    room_random.room_occupants.append(person)
                    self.persons_total.append(person)
                    room_living = random.choice(self.living_space)
                    if len(room_living.room_occupants) <= room_living.room_size:
                        print("{} has been added to the living room {} ".format(person.person_name,
                                                                                room_living.room_name))
                        room_living.room_occupants.append(person)

                if person_accomodation == "N":
                    print("{0} has been added to the office {1} ".format(person.person_name,
                                                                         room_random.room_name))
                    room_random.room_occupants.append(person)
                    self.persons_total.append(person)

        except IndexError:
            self.unallocated.append(person)
            print("You have no rooms to start with , add rooms first")

    def print_room(self, room_name):

        if room_name not in [room.room_name for room in self.rooms]:
            print("Sorry.That room does not exist.")
        else:
            for room_to_check in self.rooms:
                if room_name == room_to_check.room_name:
                    if len(room_to_check.room_occupants) > 0:
                        for occupant in room_to_check.room_occupants:
                            print(occupant.person_name)
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
            elif filename not in [file for file in os.listdir("/Users/farhanabdi/dojo-room-allocation")]:
                files = [file for file in os.listdir("/Users/farhanabdi/dojo-room-allocation")
                         if file.endswith(".txt") and not file.startswith("requirements")]
                if len(files) > 0:
                    print("You have already created a file for the system using it instead " + files[0])
                    doc = open(files[0], "a+")
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

    def print_unallocated(self, filename=None):
        if filename is None:
            if not self.rooms:
                print("Sorry.No rooms exist. Please create one")
                for room in self.unallocated:
                    print(room.person_name)
            else:
                for room in self.unallocated:
                    print(room.person_name)

        elif filename not in os.listdir("/Users/farhanabdi/dojo-room-allocation"):
            doc = open(filename, "a+")
            for room in self.unallocated:
                doc.write(room.person_name)
                doc.close()
        else:
            doc = open(filename, "a+")
            for room in self.unallocated:
                doc.write(room.person_name)
                doc.close()

    def reallocate_person(self, person_name, room_name):
        if room_name not in [room.room_name for room in self.rooms]:
            print(" this Doesnt exist")
        else:
            if person_name not in [person.person_name for person in self.persons_total]:
                print("This name not in rooms")
            person_names = [person.person_name for person in self.persons_total
                            if person_name in person.person_name]
            if len(person_names) == 1:
                for person in self.persons_total:
                    if person.person_name == person_names[0]:
                        person_to_move = person
                        for room in self.rooms:

                            if person_to_move in room.room_occupants:
                                room_from = room
                                print("From room " + str(room_from))
                        for room in self.rooms:
                            if room.room_name == room_name:
                                room_to = room
                                if room_from.room_type == room_to.room_type:
                                    print("moving human...")
                                    room.room_occupants.append(person_to_move)
                                else:
                                    print("Cannot move into different room types")
                                    room_from.room_occupants.append(person_to_move)
            elif len(person_names) > 1:
                for i, name in enumerate(person_names, 0):
                    print(i, name)
                print("\n" + "please enter the number of the person you want to move")
                int_person = int(input(">>>enter the number"))
                print(person_names[int_person])
                for person in self.persons_total:
                    if person_names[int_person] in person.person_name:
                        person_to_move = person

                for room in self.rooms:

                    if person_to_move in room.room_occupants:
                        room_from = room
                        room.room_occupants.remove(person_to_move)
                for room in self.rooms:
                    if room.room_name == room_name:
                        room_to = room
                        if room_from.room_type == room_to.room_type:
                            print("Adding person to new room")
                            if len(room_to.room_occupants) < room_to.room_size:
                                room.room_occupants.append(person_to_move)
                            else:
                                print("sorry this room is full ")
                                room_from.room_occupants.append(person_to_move)
                        else:
                            print("Cannot move into different room types")
                            room_from.room_occupants.append(person_to_move)

    def load_people(self, filename=None):
        if filename is None:
            print("Select the file from the pop up window")
            root = tk.Tk()
            root.withdraw()
            root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                       filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
            print("Copying files to the csv folder")
            try:
                copy(root.filename, "/Users/farhanabdi/dojo-room-allocation/csvs")
                print("Done copying")
                print("reading file.please wait...")
                people_list = open(root.filename).readlines()
                print(people_list)
                for line in people_list:
                    person_details = line.split()
                    if len(person_details) == 4:
                        f_name = person_details[0]
                        s_name = person_details[1]
                        full_name = f_name + s_name
                        p_type = person_details[2]
                        p_accomodation = person_details[3]
                        self.add_persons(full_name, p_type, p_accomodation)
                    if len(person_details) == 3:
                        f_name = person_details[0]
                        s_name = person_details[1]
                        full_name = f_name + s_name
                        p_type = person_details[2]
                        p_accomodation = "N"
                        self.add_persons(full_name, p_type, p_accomodation)
            except IOError as why:
                print(str(why))
                print("file already in csv directory.just run the function with the file name")

        else:
            if filename in os.listdir("/Users/farhanabdi/dojo-room-allocation/csvs"):
                print(filename)
                people_list = open("/Users/farhanabdi/dojo-room-allocation/csvs/"+filename).readlines()
                print(people_list)
                for line in people_list:

                    person_details = line.split()

                    if len(person_details) == 4:
                        f_name = person_details[0]
                        s_name = person_details[1]
                        full_name = f_name + s_name
                        p_type = person_details[2]
                        p_accomodation = person_details[3]
                        self.add_persons(full_name, p_type, p_accomodation)
                    if len(person_details) == 3:
                        f_name = person_details[0]
                        s_name = person_details[1]
                        full_name = f_name + s_name
                        p_type = person_details[2]
                        p_accomodation = "N"
                        self.add_persons(full_name, p_type, p_accomodation)
            else:
                print("file not in csv directory")

    def save_state(self, filename=None):
        if not filename:
            db_name = 'sqlite:///' + os.path.join(db_room.base_dir, 'dojo.db')
            engine = create_engine(db_name)
            metadata = MetaData(bind=db_room.engine)
            session = sessionmaker(bind=engine)
            s = session()

            for room in self.rooms:

                if s.query(db_room.Rooms).filter(room.room_name == db_room.Rooms.room_name).count():
                    print("this room is existing ...")
                    query_size = s.query(db_room.Persons).filter(db_room.Rooms.room_name ==
                                                                         db_room.Persons.room_name)
                    list_people = query_size.all()
                    print(len(list_people))

                    if len(list_people) < room.room_size:
                        print("This rooms exists but has space in it adding this person here :)")
                        last_person = self.persons_total[-1]
                        print("last person")
                        print(last_person.person_name)
                        tbl = Table(db_room.Persons.__tablename__, metadata, autoload=True)
                        p_table = tbl.insert()
                        new_person = p_table.values(person_name=last_person.person_name,
                                                    person_type=last_person.role,
                                                    person_accomodation=last_person.person_accomodation,
                                                    room_name=room.room_name,
                                                    room_type=room.room_type,
                                                    )
                        conn = db_room.engine.connect()
                        conn.execute(new_person)

                    else:
                        print("This room is full and is already in the db :(")
                        print("This room exists already")

                else:
                    print(room)
                    rms = db_room.Rooms(room_name=room.room_name, room_type=room.room_type)
                    s.add(rms)
                    s.commit()
                    for occupant in room.room_occupants:
                        prs = db_room.Persons(person_name=occupant.person_name, person_type=occupant.role,
                                              person_accomodation=occupant.person_accomodation,
                                              room_name=room.room_name, room_type=room.room_type, rooms=rms)
                        s.add(prs)
                        s.commit()

        else:
            engine = create_engine('sqlite:///{}.db'.format(filename))
            db_room.base.metadata.create_all(engine)
            session = sessionmaker(bind=engine)
            s = session()
            metadata = MetaData(bind=db_room.engine)

            for room in self.rooms:

                print(room)
                rms = db_room.Rooms(room_name=room.room_name, room_type=room.room_type)
                s.add(rms)
                s.commit()
                for occupant in room.room_occupants:
                    prs = db_room.Persons(person_name=occupant.person_name, person_type=occupant.role,
                                          person_accomodation=occupant.person_accomodation,
                                          room_name=room.room_name, room_type=room.room_type, rooms=rms)
                    s.add(prs)
                    s.commit()

    def load_state(self, filename=None):
        if filename is None:
            db_name = 'sqlite:///' + os.path.join(db_room.base_dir, 'dojo.db')
            engine = create_engine(db_name)
            metadata = MetaData(bind=db_room.engine)
            session = sessionmaker(bind=engine)
            s = session()
            list_room = s.query(db_room.Persons).all()
            for person in list_room:

                rm_name = person.room_name
                rm_type = person.room_type
                person_type = person.person_type
                print("rm_nm n type")
                print(rm_name)
                print(rm_type)
                print("printing person.room")
                if rm_type == "office":
                    room_create = Office(person.room_name)
                    if person_type == "STAFF":
                        staff_obj = Staff(person_name=person.person_name)
                        room_create.room_occupants.append(staff_obj)
                        self.rooms.append(room_create)
                        self.offices.append(room_create)
                        self.persons_total.append(staff_obj)
                        self.allocated.append(staff_obj)
                        print(len(self.rooms))
                    else:
                        print("Fellow")
                        staff_obj = Fellow(person_name=person.person_name,
                                           person_accomodation=person.person_accomodation)
                        room_create.room_occupants.append(staff_obj)
                        self.rooms.append(room_create)
                        self.offices.append(room_create)
                        self.persons_total.append(staff_obj)
                        self.allocated.append(staff_obj)

        else:
            db_name = 'sqlite:///{}'.format(filename)
            engine = create_engine(db_name)
            metadata = MetaData(bind=db_room.engine)
            session = sessionmaker(bind=engine)
            s = session()
            list_room = s.query(db_room.Persons).all()
            for person in list_room:

                rm_name = person.room_name
                rm_type = person.room_type
                person_type = person.person_type
                print("rm_nm n type")
                print(rm_name)
                print(rm_type)
                print("printing person.room")
                if rm_type == "office":
                    room_create = Office(person.room_name)
                    if person_type == "STAFF":
                        staff_obj = Staff(person_name=person.person_name)
                        room_create.room_occupants.append(staff_obj)
                        self.rooms.append(room_create)
                        self.offices.append(room_create)
                        self.persons_total.append(staff_obj)
                        self.allocated.append(staff_obj)
                        print(len(self.rooms))
                    else:
                        print("Fellow")
                        staff_obj = Fellow(person_name=person.person_name,
                                           person_accomodation=person.person_accomodation)
                        room_create.room_occupants.append(staff_obj)
                        self.rooms.append(room_create)
                        self.offices.append(room_create)
                        self.persons_total.append(staff_obj)
                        self.allocated.append(staff_obj)

