#!/usr/bin/python3
"""Amenity class module Test"""
from unittest import TestCase
from datetime import datetime
from models.amenity import Amenity
from unittest.mock import patch, mock_open


class TestAmenity(TestCase):
    """Amenity class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'Amenity',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.a_1 = Amenity(name="1")
        self.a_2 = Amenity(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.a_1.id, str)
        self.assertIsInstance(self.a_1.name, str)
        self.assertNotEqual(self.a_1.id, self.a_2.id)
        self.assertIsInstance(self.a_1.created_at, datetime)
        self.assertIsInstance(self.a_1.updated_at, datetime)
        self.assertNotEqual(self.a_1.created_at, self.a_2.created_at)
        self.assertNotEqual(self.a_1.updated_at, self.a_2.updated_at)
        self.assertEqual(self.a_1.created_at, self.a_1.updated_at)
        self.assertEqual(self.a_2.created_at, self.a_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[Amenity] ({self.a_1.id}) {self.a_1.__dict__}"
        self.assertEqual(string, str(self.a_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.a_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.a_1.created_at, self.a_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.a_1.to_dict()
        self.assertEqual(new_dict["__class__"], "Amenity")
        self.assertEqual(new_dict["id"], self.a_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.a_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.a_1.updated_at.isoformat())
