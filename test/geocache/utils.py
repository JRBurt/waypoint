import unittest
from geocache import utils


class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_in(self):
        test_dict = {"hello": {"world": 4}, "foo": "bar", "bizz": {"bang"}}
        self.assertEqual(utils.get_in(test_dict, ["hello", "world"]), 4)
        self.assertEqual(utils.get_in(test_dict, ["foo"]), "bar")
        self.assertEqual(utils.get_in(test_dict, ["bizz"]), {"bang"})

    def test_slugify(self):
        test_cases = [
            ("Test Widget Resize", "test widget resize"),
            ("Slugsy-43", "slugsy43"),
        ]
        for ts in test_cases:
            case, expected = ts
            self.assertEqual(utils.slugify(case), expected)
