#!/usr/bin/python3
"""Place class module Test"""
from unittest import TestCase
from datetime import datetime
from models.place import Place
from unittest.mock import patch, mock_open


class TestPlace(TestCase):
    """Place class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'Place',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.p_1 = Place()
        self.p_2 = Place(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.p_1.id, str)
        self.assertIsInstance(self.p_1.city_id, str)
        self.assertIsInstance(self.p_1.user_id, str)
        self.assertIsInstance(self.p_1.name, str)
        self.assertIsInstance(self.p_1.description, str)
        self.assertIsInstance(self.p_1.number_rooms, int)
        self.assertIsInstance(self.p_1.number_bathrooms, int)
        self.assertIsInstance(self.p_1.max_guest, int)
        self.assertIsInstance(self.p_1.price_by_night, int)
        self.assertIsInstance(self.p_1.latitude, float)
        self.assertIsInstance(self.p_1.longitude, float)
        self.assertIsInstance(self.p_1.amenity_ids, list)
        self.assertNotEqual(self.p_1.id, self.p_2.id)
        self.assertIsInstance(self.p_1.created_at, datetime)
        self.assertIsInstance(self.p_1.updated_at, datetime)
        self.assertNotEqual(self.p_1.created_at, self.p_2.created_at)
        self.assertNotEqual(self.p_1.updated_at, self.p_2.updated_at)
        self.assertEqual(self.p_1.created_at, self.p_1.updated_at)
        self.assertEqual(self.p_2.created_at, self.p_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[Place] ({self.p_1.id}) {self.p_1.__dict__}"
        self.assertEqual(string, str(self.p_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.p_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.p_1.created_at, self.p_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.p_1.to_dict()
        self.assertEqual(new_dict["__class__"], "Place")
        self.assertEqual(new_dict["id"], self.p_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.p_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.p_1.updated_at.isoformat())
