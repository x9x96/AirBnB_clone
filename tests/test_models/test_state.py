#!/usr/bin/python3
"""State class module Unittest"""
import unittest
import os
import re
import pep8
import json
import time
from models import storage
from datetime import datetime
from models.state import State
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestState(unittest.TestCase):
    """Test Cases for the State class."""

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

    def test_instantiation(self):
        """
        Test if an instance is of the correct class and inheritance.
        """
        state = State()
        self.assertEqual(str(type(state)), "<class 'models.state.State'>")
        self.assertIsInstance(state, State)
        self.assertTrue(issubclass(type(state), BaseModel))

    def test_attributes(self):
        """
        Test the existence and type of attributes.
        """
        attributes = storage.attributes()["State"]
        state = State()
        for key, value in attributes.items():
            self.assertTrue(hasattr(state, key))
            self.assertEqual(type(getattr(state, key, None)), value)

    def test_pep8(self):
        """
        Test if the code complies with PEP8 style guidelines.
        """
        py_code_style = pep8.StyleGuide(quiet=True)
        path_user = 'models/state.py'
        result = py_code_style.check_files([path_user])
        self.assertEqual(result.total_errors, 0, "errors found.")

    def test_doc_state_class(self):
        """
        Test if State class has documentation.
        """
        self.assertTrue(len(State.__doc__) > 0)

    def test_doc_state_methods(self):
        """
        Test if State methods have documentation.
        """
        for method in dir(State):
            self.assertTrue(len(getattr(State, method).__doc__) > 0)


if __name__ == "__main__":
    unittest.main()
