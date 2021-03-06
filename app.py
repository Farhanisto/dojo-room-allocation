"""
Dojo

Usage:
     Dojo create_room  <room_type> <room_name>...
     Dojo add_persons <name> <role> [<wants_accommodation>]
     Dojo print_room  <room_name>
     Dojo print_allocations  [<file_name>]
     Dojo quit


Options:
    -i, --interactive  Interactive Mode
    -h, --help Show this screen and exit
"""

import cmd
from dojo import Dojo
from docopt import docopt, DocoptExit



def docopt_cmd(func):

    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class App(cmd.Cmd):
    print("WELCOME TO DOJO ROOM ALLOCATION")
    print("")
    print("ROOM ALLOCATION COMMANDS")
    print("")
    print("1.  create_room <room_type> <room_name> ...")
    print("2.  add_persons <name> <role> [<wants_accommodation>]")
    print("3.  print_room <room_name>")
    print("4.  print_allocations [<file_name>]")
    print("5. quit")
    print("")

    prompt = '(Dojo)'
    dojo = Dojo()

    @docopt_cmd
    def do_create_room(self, arg):

        """
        Usage: create_room <room_type> <room_name>...
        """
        room_name = arg["<room_name>"]
        room_type = arg["<room_type>"]
        if room_name and room_type:
            self.dojo.create_room(room_type,room_name)

    @docopt_cmd
    def do_add_persons(self, arg):

        """
        Usage: add_persons <first_name> <role> [<wants_accommodation>]
        """

        first_name = arg["<first_name>"]
        role = arg["<role>"].upper()
        accommodation = arg["<wants_accommodation>"]
        if accommodation is None:
            accommodation = "N"

        accommodation.upper()
        self.dojo.add_persons(first_name, role, accommodation)

    @staticmethod
    def do_quit(self):

        """ Quits out of program"""

        print('Thank you for using Dojo!')
        print('See you next time!')
        print('THIS IS ANDELA')
        exit()

    @docopt_cmd
    def do_print_room(self, arg):
        """
        Usage: print_room <room_name>
        """
        room_name = arg["<room_name>"]
        if room_name is not None:
            self.dojo.print_room(room_name)

    @docopt_cmd
    def do_print_allocations(self, arg):

        """
        Usage: print_allocations [<filename>]
        """
        self.dojo.print_allocations(arg["<filename>"])


if __name__ == "__main__":
    try:
        App().cmdloop()
    except KeyboardInterrupt:
        print("Have a nice day")
        print("THIS IS ANDELA")
