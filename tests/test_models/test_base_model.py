#!/usr/bin/python3
"""TestBaseModel module Unittest"""
from datetime import datetime
import unittest
from models.base_model import BaseModel
import pep8


class TestBaseModel(unittest.TestCase):
    """Test cases for the BaseModel class."""

    def setUp(self):
        """Set up the test environment."""
        pass

    def test_type_of_id(self):
        """Test the type of the 'id' attribute."""
        model = BaseModel()
        self.assertTrue(type(model.id) == str)

    def test_type_of_datetime(self):
        """Test the type of the 'created_at' and 'updated_at' attributes."""
        model = BaseModel()
        self.assertTrue(type(model.created_at) == datetime)
        self.assertTrue(type(model.updated_at) == datetime)

    def test_str(self):
        """Test the __str__() method."""
        model = BaseModel()
        expected_str = "[" + model.__class__.__name__ + "]" + " (
            " + model.id + ") " + str(model.__dict__)
        self.assertEqual(model.__str__(), expected_str)

    def test_uuid_generation(self):
        """Test the generation of unique UUIDs."""
        model1 = BaseModel()
        model2 = BaseModel()
        model3 = BaseModel()
        self.assertTrue(model1.id != model2.id)
        self.assertTrue(model2.id != model3.id)
        self.assertTrue(model3.id != model1.id)

    def test_to_dict(self):
        """Test the to_dict() method."""
        model = BaseModel()
        my_model = model.to_dict()
        self.assertTrue(type(my_model["created_at"]) == str)
        self.assertTrue(type(my_model["updated_at"]) == str)
        self.assertTrue(type(model.created_at) == datetime)
        self.assertTrue(type(model.updated_at) == datetime)
        self.assertEqual(my_model["created_at"], model.created_at.isoformat())
        self.assertEqual(my_model["updated_at"], model.updated_at.isoformat())

    def test_none_dict(self):
        """Test instantiation with None argument."""
        model = BaseModel(None)
        self.assertTrue(type(model.id) == str)
        self.assertTrue(type(model.created_at) == datetime)
        self.assertTrue(type(model.updated_at) == datetime)

    def test_kwargs_with_dict(self):
        """Test instantiation with **kwargs from a dictionary."""
        my_model = BaseModel()
        my_model_json = my_model.to_dict()
        my_new_model = BaseModel(**my_model_json)
        self.assertEqual(my_model_json, my_new_model.to_dict())
        self.assertTrue(type(my_new_model.id) == str)
        self.assertTrue(type(my_new_model.created_at) == datetime)
        self.assertTrue(type(my_new_model.updated_at) == datetime)

    def test_kwargs_with_emp_dict(self):
        """Test instantiation with empty **kwargs dictionary."""
        my_dict = {}
        my_model = BaseModel(**my_dict)
        self.assertTrue(type(my_model.id) == str)
        self.assertTrue(type(my_model.created_at) == datetime)
        self.assertTrue(type(my_model.updated_at) == datetime)

    def test_pep8(self):
        """Test if the code complies with PEP8 style guidelines."""
        py_code_style = pep8.StyleGuide(quiet=True)
        check = py_code_style.check_files([
            'models/base_model.py', 'tests/test_models/test_base_model.py'])
        self.assertEqual(check.total_errors, 0, "errors found.")

    def test_doc_base_model_class(self):
        """Test if BaseModel class has documentation."""
        self.assertTrue(len(BaseModel.__doc__) > 0)

    def test_doc_base_model_methods(self):
        """Test if BaseModel methods have documentation."""
        for method_name in dir(BaseModel):
            method = getattr(BaseModel, method_name)
            self.assertTrue(len(method.__doc__) > 0)


if __name__ == '__main__':
    unittest.main()
