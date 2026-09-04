import unittest

from markdown_conversion import markdown_to_textnodes
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

    if __name__ == "__main__":
        unittest.main()
