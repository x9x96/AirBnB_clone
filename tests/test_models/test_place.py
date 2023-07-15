#!/usr/bin/python3
"""Place class module Unittest"""
import unittest
import os
import re
import pep8
import json
import time
from models import storage
from datetime import datetime
from models.place import Place
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestPlace(unittest.TestCase):
    """Test cases for the Place class."""

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

    def test_is_instance(self):
        """
        Test if an instance is of the correct class and inheritance.
        """
        place = Place()
        self.assertEqual(str(type(place)), "<class 'models.place.Place'>")
        self.assertIsInstance(place, Place)
        self.assertTrue(issubclass(type(place), BaseModel))

    def test_attributes(self):
        """
        Test the existence and type of attributes.
        """
        attributes = storage.attributes()["Place"]
        place = Place()
        for key, value in attributes.items():
            self.assertTrue(hasattr(place, key))
            self.assertEqual(type(getattr(place, key, None)), value)

    def test_pep8(self):
        """
        Test if the code complies with PEP8 style guidelines.
        """
        py_code_style = pep8.StyleGuide(quiet=True)
        path_user = 'models/place.py'
        result = py_code_style.check_files([path_user])
        self.assertEqual(result.total_errors, 0, "errors found.")

    def test_doc_place_class(self):
        """
        Test if Place class has documentation.
        """
        self.assertTrue(len(Place.__doc__) > 0)

    def test_doc_place_methods(self):
        """
        Test if Place methods have documentation.
        """
        for method in dir(Place):
            self.assertTrue(len(getattr(Place, method).__doc__) > 0)
