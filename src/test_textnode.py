from typing import Optional
import unittest
from textnode import TextNode, TextType


class AnotherObject:
    def __init__(
        self, text: str, text_type: TextType, url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a url node", TextType.LINK, "google.com")
        node2 = TextNode("This is a url node", TextType.BOLD, "google.com")
        node3 = TextNode("This is a url node 2", TextType.LINK, "google.com")
        node4 = TextNode("This is a url node", TextType.LINK, "google2.com")

        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)

    def test_other_objects_not_eq(self):
        textnode = TextNode("I am a node!", TextType.BOLD)
        foreignObject = AnotherObject("I am a node!", TextType.BOLD)
        self.assertNotEqual(textnode, foreignObject)

    def test_url_default_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node.url, None)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.google.com")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.google.com)", repr(node)
        )


if __name__ == "__main__":
    unittest.main()
