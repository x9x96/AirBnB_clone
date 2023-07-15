#!/usr/bin/python3
"""HBNB class module Unittest"""
import re
import os
import sys
import json
import unittest
import datetime
from io import StringIO
from unittest.mock import patch
from console import HBNBCommand
from models.engine.file_storage import FileStorage


class TestHBNBCommand(unittest.TestCase):
    """
    Test case for the HBNB console.
    """

    attribute_values = {
        str: "foobar108",
        int: 1008,
        float: 1.08
    }

    reset_values = {
        str: "",
        int: 0,
        float: 0.0
    }

    test_random_attributes = {
        "strfoo": "barfoo",
        "intfoo": 248,
        "floatfoo": 9.8
    }

    @classmethod
    def setUpClass(cls):
        """Set up the test class."""
        if os.path.isfile("file.json"):
            os.remove("file.json")
        cls.resetStorage()

    @classmethod
    def resetStorage(cls):
        """Reset the FileStorage."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def setUp(self):
        """Set up each individual test."""
        self.resetStorage()

    def test_help(self):
        """Test the 'help' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("help")
        s = """
Documented commands (type help <topic>):
========================================
EOF  all  count  create  destroy  help  quit  show  update

"""
        self.assertEqual(s, f.getvalue())

    def test_help_command(self, command):
        """Test the 'help' command for a specific command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"help {command}")
        expected_output = f"{command.capitalize()} description\n        \n"
        self.assertEqual(expected_output, f.getvalue())

    def test_help_commands(self):
        """Test the 'help' command for all commands."""
        commands = ["EOF", "quit", "create", "show", "destroy", "all", "count", "update"]
        for command in commands:
            self.test_help_command(command)

    def test_do_quit(self):
        """Test the 'quit' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("quit garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 0)
        self.assertEqual("", msg)

    def test_do_EOF(self):
        """Test the 'EOF' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("EOF garbage")
        msg = f.getvalue()
        self.assertTrue(len(msg) == 1)
        self.assertEqual("\n", msg)

    def test_emptyline(self):
        """Test an empty line input."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("\n")
        s = ""
        self.assertEqual(s, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("                  \n")
        s = ""
        self.assertEqual(s, f.getvalue())

    def test_do_create(self):
        """Test the 'create' command."""
        for classname in self.classes():
            self.help_test_do_create(classname)

    def help_test_do_create(self, classname):
        """Helper method for testing the 'create' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)
        key = f"{classname}.{uid}"
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"all {classname}")
        self.assertTrue(uid in f.getvalue())

    def test_do_create_error(self):
        """Test error cases for the 'create' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("create garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_show(self):
        """Test the 'show' command."""
        for classname in self.classes():
            self.help_test_do_show(classname)
            self.help_test_show_advanced(classname)

    def help_test_do_show(self, classname):
        """Helper method for testing the 'show' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show {classname} {uid}")
        s = f.getvalue()[:-1]
        self.assertTrue(uid in s)

    def test_do_show_error(self):
        """Test error cases for the 'show' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("show BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def help_test_show_advanced(self, classname):
        """Helper method for testing the 'show' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"{classname}.show('{uid}')")
        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_do_show_error_advanced(self):
        """Test error cases for the 'show' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.show('6524359')")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_destroy(self):
        """Test the 'destroy' command."""
        for classname in self.classes():
            self.help_test_do_destroy(classname)

    def help_test_do_destroy(self, classname):
        """Helper method for testing the 'destroy' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"destroy {classname} {uid}")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show {classname} {uid}")
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

    def test_do_destroy_error(self):
        """Test error cases for the 'destroy' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("destroy BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_destroy_advanced(self):
        """Test the 'destroy' command using advanced syntax."""
        for classname in self.classes():
            self.help_test_do_destroy_advanced(classname)

    def help_test_do_destroy_advanced(self, classname):
        """Helper method for testing the 'destroy' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"{classname}.destroy('{uid}')")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"show {classname} {uid}")
        s = f.getvalue()[:-1]
        self.assertTrue(len(s) == 0)

    def test_do_destroy_error_advanced(self):
        """Test error cases for the 'destroy' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.destroy('6524359')")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

    def test_do_all(self):
        """Test the 'all' command."""
        for classname in self.classes():
            self.help_test_do_all(classname)

    def help_test_do_all(self, classname):
        """Helper method for testing the 'all' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"all {classname}")
        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_do_all_error(self):
        """Test error cases for the 'all' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("all garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_all_advanced(self):
        """Test the 'all' command using advanced syntax."""
        for classname in self.classes():
            self.help_test_do_all_advanced(classname)

    def help_test_do_all_advanced(self, classname):
        """Helper method for testing the 'all' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"{classname}.all()")
        s = f.getvalue()
        self.assertTrue(uid in s)

    def test_do_all_error_advanced(self):
        """Test error cases for the 'all' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.all()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_count(self):
        """Test the 'count' command."""
        for classname in self.classes():
            self.help_test_do_count(classname)

    def help_test_do_count(self, classname):
        """Helper method for testing the 'count' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"count {classname}")
        s = f.getvalue()[:-1]
        self.assertEqual(s, "1")

    def test_do_count_error(self):
        """Test error cases for the 'count' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("count garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_count_advanced(self):
        """Test the 'count' command using advanced syntax."""
        for classname in self.classes():
            self.help_test_do_count_advanced(classname)

    def help_test_do_count_advanced(self, classname):
        """Helper method for testing the 'count' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"{classname}.count()")
        s = f.getvalue()[:-1]
        self.assertEqual(s, "1")

    def test_do_count_error_advanced(self):
        """Test error cases for the 'count' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.count()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

    def test_do_update(self):
        """Test the 'update' command."""
        for classname in self.classes():
            self.help_test_do_update(classname)

    def help_test_do_update(self, classname):
        """Helper method for testing the 'update' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        for attribute, value in self.test_random_attributes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"update {classname} {uid} {attribute} {value}")

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {classname} {uid}")
            s = f.getvalue()
            self.assertTrue(re.search(f"{attribute}': '{value}", s))

    def test_do_update_error(self):
        """Test error cases for the 'update' command."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update garbage")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 6524359")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("update BaseModel 6524359 name")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def help_test_do_update_advanced(self, classname):
        """Helper method for testing the 'update' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(f"create {classname}")
        uid = f.getvalue()[:-1]
        self.assertTrue(len(uid) > 0)

        for attribute, value in self.test_random_attributes.items():
            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"{classname}.update('{uid}', '{attribute}', '{value}')")

            with patch('sys.stdout', new=StringIO()) as f:
                HBNBCommand().onecmd(f"show {classname} {uid}")
            s = f.getvalue()
            self.assertTrue(re.search(f"{attribute}': '{value}", s))

    def test_do_update_error_advanced(self):
        """Test error cases for the 'update' command using advanced syntax."""
        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(".update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("garbage.update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update()")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** instance id missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update('6524359')")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** no instance found **")

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd("BaseModel.update('6524359', 'name')")
        msg = f.getvalue()[:-1]
        self.assertEqual(msg, "** value missing **")

    def classes(self):
        """Get the list of classes to test."""
        return ["BaseModel", "User", "State", "City", "Amenity", "Place", "Review"]


if __name__ == "__main__":
    unittest.main()
