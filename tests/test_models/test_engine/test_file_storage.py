#!/usr/bin/python3
"""FileStorage class module Unittest"""
import os
import pep8
import unittest
from models import storage
from models.base_model import BaseModel
from models.engine import file_storage
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """
    Test case for the FileStorage class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the test case by creating a FileStorage
        instance and a BaseModel instance.
        """
        cls.file_stor = FileStorage()
        cls.model = BaseModel()
        cls.file_stor.new(cls.model)
        cls.file_stor.save()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the test case by removing the
        "file.json" created during setup.
        """
        os.remove("file.json")

    def test_pep8(self):
        """
        Test the code against PEP8 style guidelines.
        """
        py_code_style = pep8.StyleGuide(quiet=True)
        check = py_code_style.check_files(
            ['models/engine/file_storage.py',
                'tests/test_models/test_engine/test_file_storage.py'])
        self.assertEqual(check.total_errors, 0, "Errors found")

    def test_is_instance(self):
        """
        Test if the FileStorage instance is an instance
        of the FileStorage class.
        """
        self.assertIsInstance(self.file_stor, FileStorage)

    def test_all(self):
        """
        Test if the return value of the all() method is a dictionary.
        """
        self.assertTrue(type(self.file_stor.all()) == dict)

    def test_new(self):
        """
        Test if a new BaseModel instance is added to the
        FileStorage's dictionary.
        """
        dict1 = self.file_stor.all()
        key = "{}.{}".format(type(self.model).__name__, self.model.id)
        self.assertTrue(key in dict1)

    def test_reload(self):
        """
        Test if the reload() method restores the dictionary
        from the saved file.
        """
        dict1 = self.file_stor.all()
        os.remove("file.json")
        self.file_stor.reload()
        dict2 = self.file_stor.all()
        self.assertEqual(dict1, dict2)

    def test_save(self):
        """
        Test if the save() and reload() methods properly
        save and restore the dictionary.
        """
        dict1 = self.file_stor.all()
        self.file_stor.save()
        self.file_stor.reload()
        dict2 = self.file_stor.all()
        key_1 = next(iter(dict1.keys()))
        key_2 = next(iter(dict2.keys()))
        self.assertEqual(dict1[key_1].to_dict(), dict2[
            key_2].to_dict())


if __name__ == '__main__':
    unittest.main()
