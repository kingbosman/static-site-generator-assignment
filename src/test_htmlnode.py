import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
        node = HTMLNode("p", "This is a paragraph")
        self.assertRaises(NotImplementedError, node.to_html)

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

    def test_parent_node_repr(self):
        node = LeafNode("p", "Hello World!")
        node2 = LeafNode("p", "Hello World2!")
        parentNode = ParentNode("div", [node, node2])
        result = f"tag:div, children:{[node,node2]}, props:None"
        self.assertEqual(repr(parentNode), result)

    def test_to_html_with_children(self):
        child = LeafNode("p", "This is p")
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><p>This is p</p></div>")

    def test_to_html_with_grand_children_and_parent_prop(self):
        grandChild = LeafNode("span", "This is a span")
        child = ParentNode("p", [grandChild], {"class": "paragraph"})
        parent = ParentNode("div", [child])
        self.assertEqual(
            parent.to_html(),
            '<div><p class="paragraph"><span>This is a span</span></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
