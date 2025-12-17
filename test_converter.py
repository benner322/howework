import unittest
import os
from converter import Parser


class TestConverter(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_parse_numbers(self):
        text = "value: 1.5e2"
        result = self.parser.parse(text)
        self.assertEqual(result['value'], 150.0)

    def test_parse_array(self):
        text = "values: [10 20 30]"
        result = self.parser.parse(text)
        self.assertEqual(result['values'], [10, 20, 30])

    def test_parse_var(self):
        text = """var x 5
value: ${x 1 +}"""
        result = self.parser.parse(text)
        self.assertEqual(result['value'], 6)

    def test_pow_function(self):
        text = """var a 2
var b 3
result: ${a b pow}"""
        result = self.parser.parse(text)
        self.assertEqual(result['result'], 8.0)

    def test_max_function(self):
        text = """var x 10
var y 15
result: ${x y max}"""
        result = self.parser.parse(text)
        self.assertEqual(result['result'], 15)


if __name__ == '__main__':
    unittest.main()