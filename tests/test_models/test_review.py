#!/usr/bin/python3
"""Review class module Unittest"""
import unittest
import os
import re
import pep8
import json
import time
from models import storage
from datetime import datetime
from models.review import Review
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestReview(unittest.TestCase):
    """Test cases for the Review class"""

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
        review = Review()
        self.assertEqual(str(type(review)), "<class 'models.review.Review'>")
        self.assertIsInstance(review, Review)
        self.assertTrue(issubclass(type(review), BaseModel))

    def test_attributes(self):
        """
        Test the existence and type of attributes.
        """
        attributes = storage.attributes()["Review"]
        review = Review()
        for key, value in attributes.items():
            self.assertTrue(hasattr(review, key))
            self.assertEqual(type(getattr(review, key, None)), value)

    def test_pep8(self):
        """
        Test if the code complies with PEP8 style guidelines.
        """
        py_code_style = pep8.StyleGuide(quiet=True)
        path_user = 'models/review.py'
        result = py_code_style.check_files([path_user])
        self.assertEqual(result.total_errors, 0, "errors found.")

    def test_doc_review_class(self):
        """
        Test if Review class has documentation.
        """
        self.assertTrue(len(Review.__doc__) > 0)

    def test_doc_review_methods(self):
        """
        Test if Review methods have documentation.
        """
        for method in dir(Review):
            self.assertTrue(len(getattr(Review, method).__doc__) > 0)
        unittest.main()
