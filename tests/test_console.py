#!/usr/bin/python3
"""HBNBCommand class module Test"""
from unittest import TestCase
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.engine.file_storage import FileStorage
from io import StringIO
from os import rename, remove
from unittest.mock import patch


class TestHBNBCommand(TestCase):
    """HBNBCommand class Test"""
    cls = ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]
    all = FileStorage().all()

    @classmethod
    def setUpClass(cls):
        """prevent altering production storage"""
        try:
            rename("file.json", "backup.json")
        except Exception:
            pass

    def test_EOF(self):
        """test EOF"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
            self.assertEqual(f.getvalue(), '\n')

    def test_quit(self):
        """test quit"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
            self.assertEqual(f.getvalue(), '')

    def test_emptyline(self):
        """test emptyline"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd('')
            self.assertEqual(f.getvalue(), '')
            f.seek(0)
            f.truncate(0)
            HBNBCommand().onecmd('\n')
            self.assertEqual(f.getvalue(), '')

    def test_help(self):
        """test help"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("?")
            str = "Documented commands (type help <topic>)"
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help EOF")
            str = "Quit command to exit the program"
            self.assertEqual(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help all")
            str = "all <class name>"
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help count")
            str = "count <class name>"
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help create")
            str = "create <class name>"
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help destroy")
            str = "destroy <class name> <id>"
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help help")
            str = 'List available commands with "help"'
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help quit")
            str = "Quit command to exit the program"
            self.assertEqual(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help show")
            str = "show <class name> <id>"
            self.assertIn(str, f.getvalue().strip())
            f.seek(0)
            f.truncate(0)

            HBNBCommand().onecmd("help update")
            str = "update <class name> <id> <attribute name> <attribute value>"
            self.assertIn(str, f.getvalue().strip())

    def test_create(self):
        """test create function"""
        with patch('sys.stdout', new=StringIO()) as f:
            """test without class name"""
            HBNBCommand().onecmd("create")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class name missing **")

            """test with incorrect class name"""
            f.seek(0)
            f.truncate(0)
            HBNBCommand().onecmd("create class")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test with correct class names"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                self.assertIn(f"{i}.{id}", self.all.keys())

    def test_all(self):
        """test all function"""
        with patch('sys.stdout', new=StringIO()) as f:
            """test without class name"""
            HBNBCommand().onecmd("all")
            objs = f.getvalue().strip()
            self.assertEqual(str([i.__str__() for i in self.all.values()]),
                             objs)

            """test with incorrect class name"""
            f.seek(0)
            f.truncate(0)
            HBNBCommand().onecmd("all class")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test with correct class names"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"all {i}")
                objs = f.getvalue().strip()
                self.assertEqual(str([j.__str__() for j in self.all.values()
                                      if type(j).__name__ == i]), objs)

    def test_check(self):
        """test check function"""
        with patch('sys.stdout', new=StringIO()) as f:
            """test without class name"""
            HBNBCommand().check("")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class name missing **")

            """test with incorrect class name"""
            f.seek(0)
            f.truncate(0)
            HBNBCommand().check(["class"])
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test with correct class names"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                """test without id"""
                HBNBCommand().check([i])
                err = f.getvalue().strip()
                self.assertEqual(err, "** instance id missing **")

                """test with incorrect id"""
                f.seek(0)
                f.truncate(0)
                HBNBCommand().check([i, "id"])
                err = f.getvalue().strip()
                self.assertEqual(err, "** no instance found **")

                """test with correct id"""
                f.seek(0)
                f.truncate(0)
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                self.assertEqual(HBNBCommand().check([i, id]), True)

    def test_show(self):
        """test show function"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                f.seek(0)
                f.truncate(0)
                HBNBCommand().onecmd(f"show {i} {id}")
                obj = f.getvalue().strip()
                self.assertEqual(obj, str(self.all.get(f"{i}.{id}")))

    def test_destroy(self):
        """test destroy function"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                self.assertIn(f"{i}.{id}", self.all.keys())
                HBNBCommand().onecmd(f"destroy {i} {id}")
                self.assertNotIn(f"{i}.{id}", self.all.keys())

    def test_update(self):
        """test update function"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                """test without attribute"""
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                f.seek(0)
                f.truncate(0)
                HBNBCommand().onecmd(f"update {i} {id}")
                err = f.getvalue().strip()
                self.assertEqual(err, "** attribute name missing **")

                """test without value"""
                f.seek(0)
                f.truncate(0)
                HBNBCommand().onecmd(f"update {i} {id} attr")
                err = f.getvalue().strip()
                self.assertEqual(err, "** value missing **")

                """test with attribute and value"""
                self.assertNotIn("test_attr_1", self.all[f"{i}.{id}"].__dict__)
                self.assertNotIn("test_attr_2", self.all[f"{i}.{id}"].__dict__)
                HBNBCommand().onecmd(f"update {i} {id} test_attr_1 test_val_1")
                HBNBCommand().onecmd(f"update {i} {id} test_attr_2 13579")
                self.assertIn("test_attr_1", self.all[f"{i}.{id}"].__dict__)
                self.assertIn("test_attr_2", self.all[f"{i}.{id}"].__dict__)
                self.assertEqual(self.all[f"{i}.{id}"].__dict__["test_attr_1"],
                                 "test_val_1")
                self.assertEqual(self.all[f"{i}.{id}"].__dict__["test_attr_2"],
                                 "13579")

    def test_count(self):
        """test count function"""
        with patch('sys.stdout', new=StringIO()) as f:
            """test without class name"""
            HBNBCommand().onecmd("count")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class name missing **")

            """test with incorrect class name"""
            f.seek(0)
            f.truncate(0)
            HBNBCommand().onecmd("count class")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"count {i}")
                count = int(f.getvalue().strip())
                self.assertEqual(len([j for j in self.all.values()
                                      if type(j).__name__ == i]), count)

    def test_default(self):
        """test default function"""

        """test <class name>.all() with incorrect class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("class.all()")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test <class name>.all() with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{i}.all()")
                objs = f.getvalue().strip()
                self.assertEqual(str([j.__str__() for j in self.all.values()
                                      if type(j).__name__ == i]), objs)

        """test <class name>.create() with incorrect class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("class.create()")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test <class name>.create() with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{i}.create()")
                id = f.getvalue().strip()
                self.assertIn(f"{i}.{id}", self.all.keys())

        """test <class name>.count() with incorrect class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("class.count()")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test <class name>.count() with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{i}.count()")
                count = int(f.getvalue().strip())
                self.assertEqual(len([j for j in self.all.values()
                                      if type(j).__name__ == i]), count)

        """test <class name>.show() with incorrect class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("class.show()")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test <class name>.show() with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                f.seek(0)
                f.truncate(0)

                """with correct id"""
                HBNBCommand().onecmd(f"{i}.show({id})")
                obj = f.getvalue().strip()
                self.assertEqual(obj, str(self.all.get(f"{i}.{id}")))
                f.seek(0)
                f.truncate(0)

                """with incorrect id"""
                HBNBCommand().onecmd(f"{i}.show(id)")
                err = f.getvalue().strip()
                self.assertEqual(err, "** no instance found **")
                f.seek(0)
                f.truncate(0)

                """without id"""
                HBNBCommand().onecmd(f"{i}.show()")
                err = f.getvalue().strip()
                self.assertEqual(err, "** instance id missing **")

        """test <class name>.destroy() with incorrect class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("class.destroy()")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test <class name>.destroy() with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                f.seek(0)
                f.truncate(0)

                """with correct id"""
                self.assertIn(f"{i}.{id}", self.all.keys())
                HBNBCommand().onecmd(f"{i}.destroy({id})")
                self.assertNotIn(f"{i}.{id}", self.all.keys())

                """with incorrect id"""
                HBNBCommand().onecmd(f"{i}.destroy(id)")
                err = f.getvalue().strip()
                self.assertEqual(err, "** no instance found **")
                f.seek(0)
                f.truncate(0)

                """without id"""
                HBNBCommand().onecmd(f"{i}.destroy()")
                err = f.getvalue().strip()
                self.assertEqual(err, "** instance id missing **")

        """test <class name>.update() with incorrect class name"""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("class.update()")
            err = f.getvalue().strip()
            self.assertEqual(err, "** class doesn't exist **")

        """test <class name>.update() with correct class name"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                f.seek(0)
                f.truncate(0)

                """with correct id, attribute and value"""
                self.assertNotIn("attribute", self.all[f"{i}.{id}"].__dict__)
                HBNBCommand().onecmd(f"{i}.update({id}, 'attribute', 'value')")
                self.assertEqual(self.all[f"{i}.{id}"].__dict__["attribute"],
                                 "value")

                """with correct id and attribute only"""
                HBNBCommand().onecmd(f"{i}.update({id}, 'attribute')")
                err = f.getvalue().strip()
                self.assertEqual(err, "** value missing **")
                f.seek(0)
                f.truncate(0)

                """with correct id only"""
                HBNBCommand().onecmd(f"{i}.update({id})")
                err = f.getvalue().strip()
                self.assertEqual(err, "** attribute name missing **")
                f.seek(0)
                f.truncate(0)

                """with incorrect id"""
                HBNBCommand().onecmd(f"{i}.update(id)")
                err = f.getvalue().strip()
                self.assertEqual(err, "** no instance found **")
                f.seek(0)
                f.truncate(0)

                """without id"""
                HBNBCommand().onecmd(f"{i}.update()")
                err = f.getvalue().strip()
                self.assertEqual(err, "** instance id missing **")

        """test update with dict"""
        for i in self.cls:
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"create {i}")
                id = f.getvalue().strip()
                dict = {"test_attr_1": "test_val_1", "test_attr_2": "13579"}
                self.assertNotIn("test_attr_1", self.all[f"{i}.{id}"].__dict__)
                self.assertNotIn("test_attr_2", self.all[f"{i}.{id}"].__dict__)
                HBNBCommand().onecmd(f"{i}.update({id}, {dict})")
                self.assertEqual(self.all[f"{i}.{id}"].__dict__["test_attr_1"],
                                 "test_val_1")
                self.assertEqual(self.all[f"{i}.{id}"].__dict__["test_attr_2"],
                                 "13579")

    @classmethod
    def tearDownClass(cls):
        """restore storage"""
        remove("file.json")
        try:
            rename("backup.json", "file.json")
        except Exception:
            pass
