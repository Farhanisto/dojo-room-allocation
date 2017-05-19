# Dojo-room-allocation
---
### intro
This is a commandline application that allows you to add rooms and people.And assigns people rooms depending on their roles. The project was developed using and runs on python 3.5 +.

<<<<<<< HEAD
[![Click here to check video of the app in usage]](https://asciinema.org/a/3ev3kc4vzvbkfgdw9uidndlvp)
=======
[![click here to view the app]](https://asciinema.org/a/3ev3kc4vzvbkfgdw9uidndlvp)
>>>>>>> release-0.1

### Getting started
---
To get started you will need to have the following
* Python version 3.5 +
* Python virtialenv
* Docopt

### Installing
---
Clone this repo by running:

   git clone https://github.com/Farhanisto/dojo-room-allocation.git

Create a virtual environment
Install dependancies:

    $ pip install -r requirements.txt

Run the app by executing

    $ python app.py

### Usage
---
    create_room <room_type> <room_name>...
Creates rooms in the Dojo. Using this command, the user should be able to create as many rooms as possible by specifying multiple room names after the create_room command.


    add_person <person_name> <FELLOW|STAFF> [wants_accommodation]
Adds a person to the system and allocates the person to a random room. wants_accommodation here is an optional argument which can be either Y or N. The default value if it is not provided is N.

    print_room <room_name>
Prints  the names of all the people in room_name on the screen.

    print_allocations [-o=filename]
Prints a list of allocations onto the screen.

### Tests
---

    To run tests, run nosetests or nosetests --with-coverage

### Built With
---

* Python - A verstile programming language
* Docopt - Python commandline arguement parser

### Authors
---

[Farhan Abdirashid](https://github.com/farhanisto)

### Acknowledgments
---
* Facilitator - Ruth Bochere Ogendi
* Andela cohort 18 participants