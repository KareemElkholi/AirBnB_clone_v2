#!/usr/bin/python3
"""City class module Test"""
from unittest import TestCase
from datetime import datetime
from models.city import City
from unittest.mock import patch, mock_open


class TestCity(TestCase):
    """City class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'City',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.city_1 = City()
        self.city_2 = City(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.city_1.id, str)
        self.assertIsInstance(self.city_1.state_id, str)
        self.assertIsInstance(self.city_1.name, str)
        self.assertNotEqual(self.city_1.id, self.city_2.id)
        self.assertIsInstance(self.city_1.created_at, datetime)
        self.assertIsInstance(self.city_1.updated_at, datetime)
        self.assertNotEqual(self.city_1.created_at, self.city_2.created_at)
        self.assertNotEqual(self.city_1.updated_at, self.city_2.updated_at)
        self.assertEqual(self.city_1.created_at, self.city_1.updated_at)
        self.assertEqual(self.city_2.created_at, self.city_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[City] ({self.city_1.id}) {self.city_1.__dict__}"
        self.assertEqual(string, str(self.city_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.city_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.city_1.created_at, self.city_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.city_1.to_dict()
        self.assertEqual(new_dict["__class__"], "City")
        self.assertEqual(new_dict["id"], self.city_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.city_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.city_1.updated_at.isoformat())
