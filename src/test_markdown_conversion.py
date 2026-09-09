import unittest

from markdown_conversion import (
    block_to_blocktype,
    extract_markdown_images,
    extraxt_markdown_links,
    markdown_to_blocks,
    markdown_to_textnodes,
    split_nodes_images_and_links,
)
from textnode import TextNode
from enums import TextType, BlockType


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

    def test_image_from_text(self):
        string = "text at the start and ![image text](https://image.png)"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("text at the start and ", TextType.TEXT),
            TextNode("image text", TextType.IMAGE, "https://image.png"),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_link_from_text(self):
        string = "text at the start and [link text](https://link.com)"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("text at the start and ", TextType.TEXT),
            TextNode("link text", TextType.LINK, "https://link.com"),
        ]
        self.assertEqual(textnodes, expectedNodes)

    def test_delims_links_images_from_text(self):
        string = "**bold** text and _italic_ text but also a `code` block. We have an ![image](https://image.png) on it finally follow this [link](https://www.link.com)"
        textnodes = markdown_to_textnodes(string)
        expectedNodes = [
            TextNode("bold", TextType.BOLD),
            TextNode(" text and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text but also a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" block. We have an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://image.png"),
            TextNode(" on it finally follow this ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.link.com"),
        ]
        self.assertListEqual(textnodes, expectedNodes)

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

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown_to_blocks(self):
        blocks = markdown_to_blocks("")
        self.assertEqual([], blocks)

    def test_multiple_new_lines_between_blocks(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

    def test_block_to_blocktype_paragraph(self):
        markdown = """This is a regular paragraph
I even have multiple lines
Amazing!
- very cool"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)

    def test_block_to_blocktype_heading(self):
        markdown = "## I am a heading!"
        self.assertEqual(block_to_blocktype(markdown), BlockType.HEADING)
        markdown = "# I am a heading!"
        self.assertEqual(block_to_blocktype(markdown), BlockType.HEADING)

    def test_block_to_blocktype_invalid_heading(self):
        markdown = "######## This is not valid"
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)
        markdown = "##This is not valid"
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)
        markdown = "This is not valid"
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)

    def test_block_to_blocktype_code(self):
        markdown = """```
Hello I am inside a code block
very cool
```"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.CODE)

    def test_block_to_blocktype_quote(self):
        markdown = """> I am a quote
> with multiple lines!"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.QUOTE)
        markdown = "> quote on single line"
        self.assertEqual(block_to_blocktype(markdown), BlockType.QUOTE)
        markdown = ">quote on single line space not required"
        self.assertEqual(block_to_blocktype(markdown), BlockType.QUOTE)

    def test_block_to_blocktype_unordered_list(self):
        markdown = """- I am an item
- so am I!"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.UNORDERED_LIST)

    def test_block_to_blocktype_ordered_list(self):
        markdown = """1. I am the first
2. Then I am second"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.ORDERED_LIST)

    def test_block_to_blocktype_invalid_ordered_list(self):
        markdown = """1. I am the first
2. Then I am second
4. Where is three? im invalid now"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)

        markdown = """1.I am the first
2.Then I am second but wait we need spaces"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)

    def test_block_to_blocktype_invalid_unordered_list(self):
        markdown = """- I am an item
-so am I! I forgot a space"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)

        markdown = """- I am an item
- so am I! I forgot a space
uh oh I dont belong"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)

    def test_block_to_blocktype_invalid_quote(self):
        markdown = """> super quote
I forgot my > sign"""
        self.assertEqual(block_to_blocktype(markdown), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
