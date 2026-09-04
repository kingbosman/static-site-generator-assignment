import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=props)
        result = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), result)

    def test_default_none(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        paragraph = HTMLNode("p", "This is a paragraph")
        title = HTMLNode("h1", "This is a title")
        children = [paragraph, title]
        props = {"class": "red"}
        node = HTMLNode(tag="div", children=children, props=props)
        result = f"tag:div, value:{None}, children:{children}, props:{props}"
        self.assertEqual(repr(node), result)

    def test_to_html_not_implemented(self):
        self.assertRaises(NotImplementedError)

    def test_leaf_node_to_html_p(self):
        node = LeafNode("p", "Hello World!")
        self.assertEqual(node.to_html(), "<p>Hello World!</p>")

    def test_leaf_node_to_html_a(self):
        node = LeafNode("a", "Hello link!", {"href": "https://www.world.com"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.world.com">Hello link!</a>'
        )

    def test_leaf_node_repr_a(self):
        node = LeafNode("a", "Hello link!", {"href": "https://www.world.com"})
        result = "tag:a, value:Hello link!, props:{'href': 'https://www.world.com'}"
        self.assertEqual(repr(node), result)

    def test_leaf_node_repr_p(self):
        node = LeafNode("p", "Hello World!")
        result = "tag:p, value:Hello World!, props:None"
        self.assertEqual(repr(node), result)
