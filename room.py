
class Room(object):
    """Creates the abstract class Room which has the living room and the office as the sub classes"""

    def __init__(self, room_name, room_type, room_size):
        self.room_name = room_name
        self.room_type = room_type
        self.room_size = room_size
        self.room_occupants = []

class Office(Room):
    def __init__(self, room_name):
        super(Office, self).__init__(room_name, room_type="office", room_size=5 )

class Living(Room):
    def __init__(self, room_name):
        super(Living, self).__init__(room_name, room_type='living', room_size=3)


