#!/usr/bin/python3
"""User class module Test"""
from unittest import TestCase
from datetime import datetime
from models.user import User
from unittest.mock import patch, mock_open


class TestUser(TestCase):
    """User class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'User',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.user_1 = User()
        self.user_2 = User(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.user_1.id, str)
        self.assertIsInstance(self.user_1.email, str)
        self.assertIsInstance(self.user_1.password, str)
        self.assertIsInstance(self.user_1.first_name, str)
        self.assertIsInstance(self.user_1.last_name, str)
        self.assertNotEqual(self.user_1.id, self.user_2.id)
        self.assertIsInstance(self.user_1.created_at, datetime)
        self.assertIsInstance(self.user_1.updated_at, datetime)
        self.assertNotEqual(self.user_1.created_at, self.user_2.created_at)
        self.assertNotEqual(self.user_1.updated_at, self.user_2.updated_at)
        self.assertEqual(self.user_1.created_at, self.user_1.updated_at)
        self.assertEqual(self.user_2.created_at, self.user_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[User] ({self.user_1.id}) {self.user_1.__dict__}"
        self.assertEqual(string, str(self.user_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.user_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.user_1.created_at, self.user_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.user_1.to_dict()
        self.assertEqual(new_dict["__class__"], "User")
        self.assertEqual(new_dict["id"], self.user_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.user_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.user_1.updated_at.isoformat())
