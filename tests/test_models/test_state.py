#!/usr/bin/python3
"""State class module Test"""
from unittest import TestCase
from datetime import datetime
from models.state import State
from unittest.mock import patch, mock_open


class TestState(TestCase):
    """State class Test"""
    def setUp(self):
        """Initialization of the test environment"""
        kwargs = {'__class__': 'State',
                  'id': '56d43177-cc5f-4d6c-a0c1-e167f8c27337',
                  'created_at': '2017-09-28T21:03:54.052298',
                  'updated_at': '2017-09-28T21:03:54.052298'}
        self.s_1 = State()
        self.s_2 = State(**kwargs)

    def test_init(self):
        """__init__ method test"""
        self.assertIsInstance(self.s_1.id, str)
        self.assertIsInstance(self.s_1.name, str)
        self.assertNotEqual(self.s_1.id, self.s_2.id)
        self.assertIsInstance(self.s_1.created_at, datetime)
        self.assertIsInstance(self.s_1.updated_at, datetime)
        self.assertNotEqual(self.s_1.created_at, self.s_2.created_at)
        self.assertNotEqual(self.s_1.updated_at, self.s_2.updated_at)
        self.assertEqual(self.s_1.created_at, self.s_1.updated_at)
        self.assertEqual(self.s_2.created_at, self.s_2.updated_at)

    def test_str(self):
        """__str__ method test"""
        string = f"[State] ({self.s_1.id}) {self.s_1.__dict__}"
        self.assertEqual(string, str(self.s_1))

    def test_save(self):
        """save method test"""
        with patch("builtins.open", mock_open()) as file:
            self.s_1.save()
            file.assert_called_with("file.json", "w")
            self.assertNotEqual(self.s_1.created_at, self.s_1.updated_at)

    def test_to_dict(self):
        """to_dict method test"""
        new_dict = self.s_1.to_dict()
        self.assertEqual(new_dict["__class__"], "State")
        self.assertEqual(new_dict["id"], self.s_1.id)
        self.assertEqual(new_dict["created_at"],
                         self.s_1.created_at.isoformat())
        self.assertEqual(new_dict["updated_at"],
                         self.s_1.updated_at.isoformat())
