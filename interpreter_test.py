import unittest

from interpreter import *


class TestInterpreter(unittest.TestCase):
    def setUp(self):
        self.interpreter = Interpreter()

    def test_string(self):
        prog = """["#", "'foo'"]"""
        result = self.interpreter.exec(prog)
        self.assertEqual(result, ["foo"])

    def test_boolean(self):
        prog = """["#", true]"""
        result = self.interpreter.exec(prog)
        self.assertEqual(result, [True])

    def test_null(self):
        prog = """["#", null]"""
        result = self.interpreter.exec(prog)
        self.assertEqual(result, [None])

    def test_add(self):
        prog = """["+", 1, 1]"""
        result = self.interpreter.exec(prog)
        self.assertEqual(result, 2)

    def test_def(self):
        prog = """
        {
            "foo": ["def", "foo", ["a", "b"], ["+", "a", "b"]],
            "x": ["foo", 1, 1]
        }
        """
        result = self.interpreter.exec(prog)
        self.assertIn("foo", result)
        self.assertEqual(result["x"], 2)

    def test_def_no_args(self):
        prog = """
        {
            "foo": ["def", "foo", [], ["+", 1, 1]],
            "x": ["foo"]
        }
        """
        result = self.interpreter.exec(prog)
        self.assertIn("foo", result)
        self.assertEqual(result["x"], 2)

    def test_let(self):
        prog = """["let", [["a", 1], ["b", 1]], ["+", "a", "b"]]"""
        result = self.interpreter.exec(prog)
        self.assertEqual(result, 2)

    def test_access(self):
        prog = """[".", {"foo": {"bar": {"baz": 1}}}, "foo", "bar", "baz"]"""
        result = self.interpreter.exec(prog)
        self.assertEqual(result, 1)

    @unittest.skip
    def test_print(self):
        prog = """["print", "'this is a test'", "'test'"]"""
        self.interpreter.exec(prog)
