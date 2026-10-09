import re
from typing import Optional
from textnode import TextNode
from enums import TextType, BlockType


def markdown_to_textnodes(rawMarkdownString: str) -> list[TextNode]:
    nodes = [TextNode(rawMarkdownString, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_images_and_links(nodes, TextType.IMAGE)
    nodes = split_nodes_images_and_links(nodes, TextType.LINK)
    return nodes


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    newNodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            newNodes.append(old_node)
            continue

        split = old_node.text.split(delimiter)

        # Should always be of length 1 or 3
        if len(split) % 2 == 0:
            raise ValueError("Invalid markdown syntax")

        for index, part in enumerate(split):
            if part == "":
                continue
            if index % 2 == 1:
                newNodes.append(TextNode(part, text_type))
                continue
            newNodes.append(TextNode(part, TextType.TEXT))

    return newNodes


def extract_markdown_images(rawMarkdownString: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", rawMarkdownString)


def extraxt_markdown_links(rawMarkdownString: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", rawMarkdownString)


def split_nodes_images_and_links(
    old_nodes: list[TextNode], text_type: TextType
) -> list[TextNode]:
    newNodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            newNodes.append(old_node)
            continue

        originalText = old_node.text
        match text_type:
            case TextType.IMAGE:
                instances = extract_markdown_images(originalText)
                prefix = "!"
            case TextType.LINK:
                instances = extraxt_markdown_links(originalText)
                prefix = ""
            case _:
                raise ValueError("Unsupported TextType")

        for instance in instances:
            altText = instance[0]
            url = instance[1]
            split = originalText.split(f"{prefix}[{altText}]({url})")

            # Second is the text_type, always
            if split[0] != "":
                newNodes.append(TextNode(split[0], TextType.TEXT))
            newNodes.append(TextNode(altText, text_type, url))
            originalText = split[1]
        if originalText != "":
            newNodes.append(TextNode(originalText, TextType.TEXT))
    return newNodes


# step 2 #


def markdown_to_blocks(rawMarkdownString: str) -> list[str]:
    # split per empty line and strip ignore empty blocks
    return [
        cleaned
        for block in rawMarkdownString.split("\n\n")
        if (cleaned := block.strip())
    ]


def block_to_blocktype(markdown: str) -> BlockType:
    if re.search(r"(^#{1,6}+ ).+", markdown):
        return BlockType.HEADING
    if re.search(r"^(`{3}\n)(.|\n)+?(\n`{3})$", markdown):
        return BlockType.CODE

    lineSplit = markdown.split("\n")

    currentBlockType = BlockType.PARAGRAPH
    if re.search(r"(^>)", markdown):
        currentBlockType = BlockType.QUOTE
    if re.search(r"(^- ).+", markdown):
        currentBlockType = BlockType.UNORDERED_LIST
    if re.search(r"(1. .+\n)", markdown):
        currentBlockType = BlockType.ORDERED_LIST
    for index, line in enumerate(lineSplit[1:], 1):
        match currentBlockType:
            case BlockType.PARAGRAPH:
                return BlockType.PARAGRAPH
            case BlockType.QUOTE:
                if not re.search(r"(^>)", line):
                    return BlockType.PARAGRAPH
            case BlockType.UNORDERED_LIST:
                if not re.search(r"(^- ).+", line):
                    return BlockType.PARAGRAPH
            case BlockType.ORDERED_LIST:
                if not re.search(rf"({index+1}. .+)", line):
                    return BlockType.PARAGRAPH

    return currentBlockType
