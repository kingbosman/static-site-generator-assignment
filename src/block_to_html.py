from typing import Optional
from enums import BlockType, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from markdown_conversion import (
    block_to_blocktype,
    markdown_to_blocks,
    markdown_to_textnodes,
)
from textnode import TextNode


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        blocktype = block_to_blocktype(block)
        headingSize = None
        if blocktype == BlockType.HEADING:
            headingSize = len(block.split(" ", 1)[0])
        blockText = strip_markdown_syntax_from_block(block, blocktype)
        tag = blocktype_to_tag(blocktype, headingSize)
        if blocktype == BlockType.CODE:
            textNode = TextNode(blockText.replace("\n", "", 1), TextType.CODE)
            children.append(ParentNode("pre", [textNode.text_node_to_html_node()]))
        elif blocktype in [BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST]:
            children.append(ParentNode(tag, lines_to_list_nodes(blockText)))
        else:
            children.append(ParentNode(tag, text_to_children_nodes(blockText)))
    return ParentNode("div", children)


def lines_to_list_nodes(text: str) -> list[HTMLNode]:
    nodes = []
    for line in text.split("\n"):
        lineNodes = text_to_children_nodes(line)
        nodes.append(ParentNode("li", lineNodes))
    return nodes


def text_to_children_nodes(text: str) -> list[HTMLNode]:
    textNodes = markdown_to_textnodes(text)
    resultNodes = []
    for node in textNodes:
        resultNodes.append(node.text_node_to_html_node())
    return resultNodes


def blocktype_to_tag(blocktype: BlockType, headingSize: Optional[int] = None) -> str:
    match blocktype:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.HEADING:
            return f"h{headingSize}"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"
    return ""


def strip_markdown_syntax_from_block(markdown: str, blocktype: BlockType) -> str:
    match blocktype:
        case BlockType.PARAGRAPH:
            return markdown.replace("\n", " ")
        case BlockType.HEADING:
            return markdown.split("# ", 1)[1]
        case BlockType.CODE:
            return markdown.split("```")[1]
        case BlockType.ORDERED_LIST | BlockType.UNORDERED_LIST | BlockType.QUOTE:
            return strip_line_item(markdown, blocktype)


def strip_line_item(lines: str, blocktype: BlockType) -> str:
    result = []
    for line in lines.split("\n"):
        match blocktype:
            case BlockType.ORDERED_LIST:
                result.append(line.split(". ", 1)[1])
            case BlockType.UNORDERED_LIST:
                result.append(line.split("- ", 1)[1])
            case BlockType.QUOTE:
                result.append(line.replace(">", "", 1).strip())
    return "\n".join(result)
