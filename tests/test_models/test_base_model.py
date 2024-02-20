#!/usr/bin/python3
"""BaseModel class module Test"""
from unittest import TestCase
from datetime import datetime
from models.base_model import BaseModel
from unittest.mock import patch, mock_open


class TestBaseModel(TestCase):
    """BaseModel class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'BaseModel',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.bm_1 = BaseModel()
        self.bm_2 = BaseModel(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.bm_1.id, str)
        self.assertNotEqual(self.bm_1.id, self.bm_2.id)
        self.assertIsInstance(self.bm_1.created_at, datetime)
        self.assertIsInstance(self.bm_1.updated_at, datetime)
        self.assertNotEqual(self.bm_1.created_at, self.bm_2.created_at)
        self.assertNotEqual(self.bm_1.updated_at, self.bm_2.updated_at)
        self.assertEqual(self.bm_1.created_at, self.bm_1.updated_at)
        self.assertEqual(self.bm_2.created_at, self.bm_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[BaseModel] ({self.bm_1.id}) {self.bm_1.__dict__}"
        self.assertEqual(string, str(self.bm_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.bm_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.bm_1.created_at, self.bm_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.bm_1.to_dict()
        self.assertEqual(new_dict["__class__"], "BaseModel")
        self.assertEqual(new_dict["id"], self.bm_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.bm_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.bm_1.updated_at.isoformat())
