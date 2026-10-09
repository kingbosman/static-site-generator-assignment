import unittest

from generator import extract_title


class testGenerator(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is a title
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        title = extract_title(md)
        self.assertEqual(title, "This is a title")

    def test_extract_title_exception(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""

        self.assertRaises(ValueError, extract_title, md)
