import unittest

from transpiler import *


class TestTranspiler(unittest.TestCase):
    def test_tokenizer(self):
        prog = """
        [def main [argc argv] [+ 1 1]]
        """
        expected = [
            "[",
            "def",
            "main",
            "[",
            "argc",
            "argv",
            "]",
            "[",
            "+",
            "1",
            "1",
            "]",
            "]",
        ]
        result = tokenize(prog)
        self.assertEqual(result, expected)

    def test_tokenizer_literals(self):
        prog = """
        [concat x #[1 2.3 -4.5e6 "baz" true false null]]
        """
        expected = [
            "[",
            "concat",
            "x",
            "#[",
            "1",
            "2.3",
            "-4.5e6",
            '"baz"',
            "true",
            "false",
            "null",
            "]",
            "]",
        ]
        result = tokenize(prog)
        self.assertEqual(result, expected)

    def test_classify_token(self):
        tokens = ["[", "[xyz", ",", '"asdf"', '"asdf', "foo", "0.123"]
        expected = [
            Token.BRACKET,
            Token.INVALID,
            Token.COMMA,
            Token.STRING,
            Token.INVALID,
            Token.IDENTIFIER,
            Token.NUMBER,
        ]
        result = [classify_token(tok) for tok in tokens]
        self.assertEqual(result, expected)
