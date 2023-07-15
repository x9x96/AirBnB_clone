#!/usr/bin/python3
"""Amenity class module Unittest"""
import unittest
import os
import re
import pep8
import json
import time
from models import storage
from datetime import datetime
from models.amenity import Amenity
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestAmenity(unittest.TestCase):
    """Test cases for the Amenity class."""

    def setUp(self):
        """Set up the test environment."""
        pass

    def tearDown(self):
        """Tear down the test environment."""
        self.resetStorage()
        pass

    def resetStorage(self):
        """Reset the FileStorage."""
        FileStorage._FileStorage__objects = {}
        if os.path.isfile(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_is_instance(self):
        """Test if an instance is of the correct class and inheritance."""
        amenity = Amenity()
        self.assertEqual(str(type(
            amenity)), "<class 'models.amenity.Amenity'>")
        self.assertIsInstance(amenity, Amenity)
        self.assertTrue(issubclass(type(amenity), BaseModel))

    def test_attributes(self):
        """Test the existence and type of attributes."""
        attributes = storage.attributes()["Amenity"]
        amenity = Amenity()
        for key, value in attributes.items():
            self.assertTrue(hasattr(amenity, key))
            self.assertEqual(type(getattr(amenity, key, None)), value)

    def test_pep8(self):
        """Test if the code complies with PEP8 style guidelines."""
        py_code_style = pep8.StyleGuide(quiet=True)
        path_user = 'models/amenity.py'
        result = py_code_style.check_files([path_user])
        self.assertEqual(result.total_errors, 0, "Errors found.")

    def test_doc_amenity_class(self):
        """Test if Amenity class has documentation."""
        self.assertTrue(len(Amenity.__doc__) > 0)

    def test_doc_amenity_methods(self):
        """Test if Amenity methods have documentation."""
        for method in dir(Amenity):
            self.assertTrue(len(method.__doc__) > 0)


if __name__ == "__main__":
    unittest.main()
