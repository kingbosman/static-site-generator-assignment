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

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, None)

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.props, None)
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.world.com")
        html_node = node.text_node_to_html_node()
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.world.com"})

    def test_image(self):
        node = TextNode(
            "This is an image node", TextType.IMAGE, "https://www.world.com/img.png"
        )
        html_node = node.text_node_to_html_node()
        self.assertEqual(
            html_node.to_html(),
            '<img src="https://www.world.com/img.png" alt="This is an image node"></img>',
        )
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.world.com/img.png", "alt": "This is an image node"},
        )

    def test_undefined_not_implemented(self):
        node = TextNode("undefined node", TextType.UNDEFINED)
        self.assertRaises(ValueError, node.text_node_to_html_node)
        self.assertRaisesRegex(
            ValueError, "Unknown TextType", node.text_node_to_html_node
        )


if __name__ == "__main__":
    unittest.main()
