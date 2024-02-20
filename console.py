#!/usr/bin/python3
"""HBNBCommand class module"""
from cmd import Cmd
from re import match
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage


class HBNBCommand(Cmd):
    """HBNBCommand class"""
    prompt = "(hbnb) "
    cls = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
    storage = FileStorage()

    def do_EOF(self, arg):
        """Quit command to exit the program"""
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Empty line + ENTER shouldn’t execute anything"""
        pass

    def do_create(self, arg):
        """Create a new instance of a class using:
        create <class name>"""
        args = split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.cls:
            print("** class doesn't exist **")
        else:
            new = eval(args[0])()
            self.storage.save()
            print(new.id)
            if len(args) > 1:
                cls = args.pop(0)
                for arg in args:
                    attr = arg.split("=")[0]
                    val = arg.split("=")[1].replace("_", " ")
                    Cmd.onecmd(self, f"update {cls} {new.id} {attr} '{val}'")


    def do_all(self, arg):
        """Print the string representation of all instances using:
        all or all <class name>"""
        args = split(arg)
        if len(args) == 0:
            print([i.__str__() for i in self.storage.all().values()])
        elif args[0] not in self.cls:
            print("** class doesn't exist **")
        else:
            print([i.__str__() for i in self.storage.all().values()
                   if type(i).__name__ == args[0]])

    def check(self, args):
        """shared if-else statement to validate the arguments"""
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.cls:
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        elif f"{args[0]}.{args[1]}" not in self.storage.all():
            print("** no instance found **")
        else:
            return True

    def do_show(self, arg):
        """Print the string representation of an instance using:
        show <class name> <id>"""
        args = split(arg)
        if self.check(args):
            print(self.storage.all().get(f"{args[0]}.{args[1]}"))

    def do_destroy(self, arg):
        """Delete an instance using:
        destroy <class name> <id>"""
        args = split(arg)
        if self.check(args):
            del self.storage.all()[f"{args[0]}.{args[1]}"]
            self.storage.save()

    def do_update(self, arg):
        """Update an instance using:
        update <class name> <id> <attribute name> <attribute value>"""
        args = split(arg)
        if self.check(args) and len(args) == 2:
            print("** attribute name missing **")
        elif len(args) == 3:
            print("** value missing **")
        elif len(args) > 3:
            obj = self.storage.all().get(f"{args[0]}.{args[1]}")
            if hasattr(obj, args[2]):
                args[3] = type(getattr(obj, args[2]))(args[3])
            try:
                setattr(obj, args[2], args[3])
            except Exception:
                pass
            self.storage.save()

    def do_count(self, arg):
        """Count instances using:
        count <class name>"""
        args = split(arg)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in self.cls:
            print("** class doesn't exist **")
        else:
            count = 0
            for i in self.storage.all().values():
                if type(i).__name__ == args[0]:
                    count += 1
            print(count)

    def default(self, arg):
        """Called when the command is not recognized"""
        if match(r"\w+?\.\w+?\(.*?\)", arg):
            fn = arg.split("(")[0].split(".")[1]
            cls = arg.split(".")[0]
            args = arg.split("{")[0].split("(")[1].replace(",", " ").strip(")")
            if "{" in arg:
                dict = arg.split("}")[0].split("{")[1].split(",")
                for i in dict:
                    attr = i.split(':')[0]
                    val = i.split(':')[1]
                    Cmd.onecmd(self, f"{fn} {cls} {args} {attr} {val}")
            else:
                Cmd.onecmd(self, f"{fn} {cls} {args}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
