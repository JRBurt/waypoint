"""python -m test"""

import unittest

import utils


class TestStringMethods(unittest.TestCase):

    test_cases = {
        1: {"input_address": "900 Washington Avenue Golden, CO 80401"},
        2: {"input_address": "HJQ2+79V Nan'An, Chongqing, China"},
    }

    def test_upper(self):
        self.assertEqual("foo".upper(), "FOO")

    def test_isupper(self):
        self.assertTrue("FOO".isupper())
        self.assertFalse("Foo".isupper())

    def test_split(self):
        s = "hello world"
        self.assertEqual(s.split(), ["hello", "world"])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)


class TestUtils(unittest.TestCase):

    foo = {"bar": {"bizz": {"bang": 5}, "bat": [1, 2, 3, 4]}}

    def test_get_in(self):
        self.assertEqual(
            utils.get_in(self.foo, ["bar"]), {"bat": [1, 2, 3, 4], "bizz": {"bang": 5}}
        )
        self.assertEqual(utils.get_in(self.foo, ["bar", "bizz"]), {"bang": 5})
        self.assertEqual(utils.get_in(self.foo, ["bar", "bat"]), [1, 2, 3, 4])
        self.assertEqual(utils.get_in(self.foo, ["bar", "bang"]), None)
        self.assertEqual(utils.get_in(self.foo, ["bar", "bizz", "bang"]), 5)


if __name__ == "__main__":
    unittest.main()
