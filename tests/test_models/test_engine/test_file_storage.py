#!/usr/bin/python3
"""FileStorage class module Test"""
from unittest import TestCase
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage
from unittest.mock import patch, mock_open


class TestFileStorage(TestCase):
    """FileStorage class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'BaseModel',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-25T21:03:54.052298',
                  'updated_at': '2017-09-25T21:03:54.052298'}
        self.model_1 = BaseModel()
        self.model_2 = BaseModel(**kwargs)
        self.storage = FileStorage()
        self.model_1.save()

    def test_all(self):
        """all method test"""
        self.assertEqual(self.storage.all(), FileStorage._FileStorage__objects)
        self.assertIsInstance(self.storage.all(), dict)
        FileStorage._FileStorage__objects.clear()
        self.assertFalse(self.storage.all())
        self.assertEqual(self.storage.all(User), {})

    def test_new(self):
        """new method test"""
        self.assertIn(f"BaseModel.{self.model_1.id}", self.storage.all())
        self.assertNotIn(f"BaseModel.{self.model_2.id}", self.storage.all())
        self.storage.new(self.model_2)
        self.assertIn(f"BaseModel.{self.model_2.id}", self.storage.all())
        with self.assertRaises(TypeError):
            self.storage.new()

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.storage.save()
            file.assert_called_with("file.json", "w")
        with self.assertRaises(TypeError):
            self.storage.save(8)

    def test_reload(self):
        """reload method test"""
        with patch("builtins.open", mock_open(read_data="{}")) as file:
            self.storage.reload()
            file.assert_called_with("file.json", "r")
        with self.assertRaises(TypeError):
            self.storage.reload(8)

    def test_delete(self):
        """delete method test"""
        self.assertIn(f"BaseModel.{self.model_1.id}", self.storage.all())
        self.storage.delete(self.model_1)
        self.storage.save()
        self.assertNotIn(f"BaseModel.{self.model_1.id}", self.storage.all())
