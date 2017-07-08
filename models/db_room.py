

from sqlalchemy import Column, Integer, String, ForeignKey,Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship,backref,sessionmaker



import os

base_dir = os.path.abspath(os.path.dirname(__file__))
db_name = 'sqlite:///' + os.path.join(base_dir, 'dojo.db')
engine = create_engine(db_name)
base = declarative_base(engine)


class Rooms(base):
    __tablename__ ='rooms'

    id = Column(Integer, primary_key=True)
    room_name = Column(String(20))
    room_type = Column(String(20))

    def __init__(self, room_name, room_type):
        self.room_name = room_name
        self.room_type = room_type

    def __repr__(self):
        return "<Room {}>".format(self.room_name)


class Persons(base):

    __tablename__ = 'persons'
    id= Column(Integer, primary_key=True)
    person_name = Column(String(25))
    person_type = Column(String(25))
    person_accomodation = Column(String(10))
    rooms_id = Column(Integer, ForeignKey('rooms.id'))
    room_name = Column(String(25))
    room_type = Column(String(25))
    rooms = relationship(Rooms, backref=backref('persons'))

    def __init__(self, person_name, person_type, person_accomodation, room_name, room_type, rooms):
        self.person_name = person_name
        self.person_type = person_type
        self.person_accomodation = person_accomodation
        self.room_name = room_name
        self.room_type = room_type
        self.rooms = rooms

    def __repr__(self):
        return "<Persons {}>".format(self.room_name)

base.metadata.create_all()



