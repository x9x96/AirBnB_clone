#!/usr/bin/python3
"""User class module Unittest"""
import unittest
import os
import re
import pep8
import json
import time
from models import storage
from datetime import datetime
from models.user import User
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestUser(unittest.TestCase):
    """Test Cases for the User class."""

    def setUp(self):
        """
        Set up the test environment.
        """
        pass

    def tearDown(self):
        """
        Tear down the test environment.
        """
        self.resetStorage()
        pass

    def resetStorage(self):
        """
        Reset the FileStorage.
        """
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_is_instantiation(self):
        """
        Test if an instance is of the correct class and inheritance.
        """
        user = User()
        self.assertEqual(str(type(user)), "<class 'models.user.User'>")
        self.assertIsInstance(user, User)
        self.assertTrue(issubclass(type(user), BaseModel))

    def test_attributes(self):
        """
        Test the existence and type of attributes.
        """
        attributes = storage.attributes()["User"]
        user = User()
        for key, value in attributes.items():
            self.assertTrue(hasattr(user, key))
            self.assertEqual(type(getattr(user, key, None)), value)

    def test_pep8(self):
        """
        Test if the code complies with PEP8 style guidelines.
        """
        py_code_style = pep8.StyleGuide(quiet=True)
        path_user = 'models/user.py'
        result = py_code_style.check_files([path_user])
        self.assertEqual(result.total_errors, 0, "errors found.")

    def test_doc_user_class(self):
        """
        Test if User class has documentation.
        """
        self.assertTrue(len(User.__doc__) > 0)

    def test_doc_user_methods(self):
        """
        Test if User methods have documentation.
        """
        for method in dir(User):
            self.assertTrue(len(getattr(User, method).__doc__) > 0)


if __name__ == "__main__":
    unittest.main()
