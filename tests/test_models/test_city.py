#!/usr/bin/python3
"""City class module Unittest"""
import unittest
import os
import re
import pep8
import json
import time
from models import storage
from datetime import datetime
from models.city import City
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestCity(unittest.TestCase):
    """Test cases for the City class."""
    def setUp(self):
        """
        Set up the test environment.
        """
        pass

    def tearDown(self):
        """
        Tear down the test environment.
        """
        self.reset_storage()
        pass

    def reset_storage(self):
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
        city = City()
        self.assertEqual(str(type(city)), "<class 'models.city.City'>")
        self.assertIsInstance(city, City)
        self.assertTrue(issubclass(type(city), BaseModel))

    def test_attributes(self):
        """
        Test the existence and type of attributes.
        """
        attributes = storage.attributes()["City"]
        city = City()
        for key, value in attributes.items():
            self.assertTrue(hasattr(city, key))
            self.assertEqual(type(getattr(city, key, None)), value)

    def test_pep8(self):
        """
        Test if the code complies with PEP8 style guidelines.
        """
        py_code_style = pep8.StyleGuide(quiet=True)
        path_user = 'models/city.py'
        result = py_code_style.check_files([path_user])
        self.assertEqual(result.total_errors, 0, "errors found.")

    def test_doc_city_class(self):
        """
        Test if City class has documentation.
        """
        self.assertTrue(len(City.__doc__) > 0)

    def test_doc_city_methods(self):
        """
        Test if City methods have documentation.
        """
        for method in dir(City):
            self.assertTrue(len(getattr(City, method).__doc__) > 0)


if __name__ == "__main__":
    unittest.main()
