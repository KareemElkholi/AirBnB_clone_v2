#!/usr/bin/python3
"""Review class module Test"""
from unittest import TestCase
from datetime import datetime
from models.review import Review
from unittest.mock import patch, mock_open


class TestReview(TestCase):
    """Review class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'Review',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.r_1 = Review(place_id="1", user_id="1", text="1")
        self.r_2 = Review(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.r_1.id, str)
        self.assertIsInstance(self.r_1.place_id, str)
        self.assertIsInstance(self.r_1.user_id, str)
        self.assertIsInstance(self.r_1.text, str)
        self.assertNotEqual(self.r_1.id, self.r_2.id)
        self.assertIsInstance(self.r_1.created_at, datetime)
        self.assertIsInstance(self.r_1.updated_at, datetime)
        self.assertNotEqual(self.r_1.created_at, self.r_2.created_at)
        self.assertNotEqual(self.r_1.updated_at, self.r_2.updated_at)
        self.assertEqual(self.r_1.created_at, self.r_1.updated_at)
        self.assertEqual(self.r_2.created_at, self.r_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[Review] ({self.r_1.id}) {self.r_1.__dict__}"
        self.assertEqual(string, str(self.r_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.r_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.r_1.created_at, self.r_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.r_1.to_dict()
        self.assertEqual(new_dict["__class__"], "Review")
        self.assertEqual(new_dict["id"], self.r_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.r_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.r_1.updated_at.isoformat())
