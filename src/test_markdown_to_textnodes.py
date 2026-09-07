import unittest

from markdown_conversion import (
    extract_markdown_images,
    extraxt_markdown_links,
    markdown_to_textnodes,
    split_nodes_images_and_links,
)
from textnode import TextNode, TextType


class TestMarkdownToTextnodes(unittest.TestCase):
    def test_no_delims_return_1_textnode(self):
        string = "This is a super simple text with no delimiters"
        textnodes = markdown_to_textnodes(string)
        self.assertEqual(textnodes, [TextNode(string, TextType.TEXT)])

    def test_bold_markdown_delim(self):
        string = "This is a super simple text with a **bold** text inside"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("This is a super simple text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text inside", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_italic_markdown_delim(self):
        string = "This is a super simple text with a _italic_ text inside"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("This is a super simple text with a ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text inside", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_code_markdown_delim(self):
        string = "This is a super simple text with a `code` text inside"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("This is a super simple text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text inside", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_delim_markdown_start(self):
        string = "**bold** text at the start"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text at the start", TextType.TEXT),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_delim_markdown_end(self):
        string = "text at the start and **bold ending**"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("text at the start and ", TextType.TEXT),
            TextNode("bold ending", TextType.BOLD),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_multiple_delims(self):
        string = "**bold** and also _italic_ but also some `interesting code` but also back to  **bold**"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" and also ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" but also some ", TextType.TEXT),
            TextNode("interesting code", TextType.CODE),
            TextNode(" but also back to  ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_extract_image_string_start(self):
        string = "![image text](https://image.png) and some text here"
        images = extract_markdown_images(string)
        self.assertEqual(images, [("image text", "https://image.png")])

    def test_extract_image_string_middle(self):
        string = "Some text here ![image text](https://image.png) and some text here"
        images = extract_markdown_images(string)
        self.assertEqual(images, [("image text", "https://image.png")])

    def test_extract_image_string_end(self):
        string = "Some text here ![image text](https://image.png)"
        images = extract_markdown_images(string)
        self.assertEqual(images, [("image text", "https://image.png")])

    def test_extract_image_string_multiple(self):
        string = "![image1 text](https://image1.png) Some text here ![image2 text](https://image2.png) and some text here ![image3 text](https://image3.png)"
        images = extract_markdown_images(string)
        self.assertEqual(
            images,
            [
                ("image1 text", "https://image1.png"),
                ("image2 text", "https://image2.png"),
                ("image3 text", "https://image3.png"),
            ],
        )

    def test_extract_image_string_does_not_extract_links(self):
        string = "![image1 text](https://image1.png) Some text here ![image2 text](https://image2.png) and some text here ![image3 text](https://image3.png) and [link](https://link.com)"
        images = extract_markdown_images(string)
        self.assertEqual(
            images,
            [
                ("image1 text", "https://image1.png"),
                ("image2 text", "https://image2.png"),
                ("image3 text", "https://image3.png"),
            ],
        )

    def test_extract_link_string_start(self):
        string = "[link text](https://link.com) and some text here"
        images = extraxt_markdown_links(string)
        self.assertEqual(images, [("link text", "https://link.com")])

    def test_extract_link_string_middle(self):
        string = "Some text here [link text](https://link.com) and some text here"
        images = extraxt_markdown_links(string)
        self.assertEqual(images, [("link text", "https://link.com")])

    def test_extract_link_string_end(self):
        string = "Some text here [link text](https://link.com)"
        images = extraxt_markdown_links(string)
        self.assertEqual(images, [("link text", "https://link.com")])

    def test_extract_link_string_multiple(self):
        string = "[link1 text](https://link1.com) Some text here [link2 text](https://link2.com) and some text here [link3 text](https://link3.com)"
        images = extraxt_markdown_links(string)
        self.assertEqual(
            images,
            [
                ("link1 text", "https://link1.com"),
                ("link2 text", "https://link2.com"),
                ("link3 text", "https://link3.com"),
            ],
        )

    def test_extract_link_string_does_not_extract_images(self):
        string = "[link1 text](https://link1.com) Some text here [link2 text](https://link2.com) and some text here [link3 text](https://link3.com) and ![image](https://image.png)"
        images = extraxt_markdown_links(string)
        self.assertEqual(
            images,
            [
                ("link1 text", "https://link1.com"),
                ("link2 text", "https://link2.com"),
                ("link3 text", "https://link3.com"),
            ],
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images_and_links([node], TextType.IMAGE)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://link.com) and another [second link](https://link2.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images_and_links([node], TextType.LINK)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://link.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://link2.com"),
            ],
            new_nodes,
        )

    if __name__ == "__main__":
        unittest.main()
