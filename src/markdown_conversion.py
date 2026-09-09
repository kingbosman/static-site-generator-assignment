import enum
import re
from textnode import BlockType, TextNode, TextType


# TODO: later at end of project support also for nested attributes
# so a bold can also be italic and vice versa etc
# do  this by finding the next instance of all delims/links/image instead
# instead of going per delim
def markdown_to_textnodes(rawMarkdownString: str) -> list[TextNode]:
    nodes = [TextNode(rawMarkdownString, TextType.TEXT)]
    delimiters = {
        TextType.BOLD: "**",
        TextType.CODE: "`",
        TextType.ITALIC: "_",
    }

    for ttype, delim in delimiters.items():
        nodes = split_nodes_delimiter(nodes, delim, ttype)
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
        newNodes.extend(
            recursive_nodes_delimiter_split(old_node.text, delimiter, text_type, [])
        )
    return newNodes


def recursive_nodes_delimiter_split(
    text: str,
    delimiter: str,
    text_type: TextType,
    current_list: list[TextNode] = [],
) -> list[TextNode]:
    split = text.split(delimiter, 2)

    # Should always be of length 1 or 3
    if len(split) == 2:
        raise ValueError("Invalid markdown syntax")

    # Nothing to split, conversion done
    if len(split) == 1:
        current_list.append(TextNode(split[0], TextType.TEXT))
        return current_list

    # second is always of type textType
    if split[0] != "":
        current_list.append(TextNode(split[0], TextType.TEXT))
    current_list.append(TextNode(split[1], text_type))

    # is last element is empty conversion is done
    if split[2] == "":
        return current_list

    # Continue splitting remaining string
    return recursive_nodes_delimiter_split(split[2], delimiter, text_type, current_list)


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
        newNodes.extend(
            recursive_nodes_images_links_split(old_node.text, text_type, [])
        )
    return newNodes


def recursive_nodes_images_links_split(
    text: str, text_type: TextType, current_list: list[TextNode]
) -> list[TextNode]:
    match text_type:
        case TextType.IMAGE:
            intances = extract_markdown_images(text)
            appendix = "!"
        case TextType.LINK:
            intances = extraxt_markdown_links(text)
            appendix = ""
        case _:
            raise ValueError("Unsupported TextType")

    # conversion done no more instances
    if len(intances) == 0:
        current_list.append(TextNode(text, TextType.TEXT))
        return current_list

    altText = intances[0][0]
    url = intances[0][1]
    split = text.split(f"{appendix}[{altText}]({url})")

    # Second is the image, always
    if split[0] != "":
        current_list.append(TextNode(split[0], TextType.TEXT))
    current_list.append(TextNode(altText, text_type, url))

    # if last element is empty conversion is done
    if split[1] == "":
        return current_list

    # Continue splitting
    return recursive_nodes_images_links_split(split[1], text_type, current_list)


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
    if re.search(r"(^>).+", markdown):
        currentBlockType = BlockType.QUOTE
    if re.search(r"(- ).+", markdown):
        currentBlockType = BlockType.UNORDERED_LIST
    if re.search(r"(1. .+\n)", markdown):
        currentBlockType = BlockType.ORDERED_LIST
    for index, line in enumerate(lineSplit[1:], 1):
        match currentBlockType:
            case BlockType.PARAGRAPH:
                return BlockType.PARAGRAPH
            case BlockType.QUOTE:
                if not re.search(r"(^>).+", line):
                    return BlockType.PARAGRAPH
            case BlockType.UNORDERED_LIST:
                if not re.search(r"(- ).+", line):
                    return BlockType.PARAGRAPH
            case BlockType.ORDERED_LIST:
                if not re.search(rf"({index+1}. .+)", line):
                    return BlockType.PARAGRAPH

    return currentBlockType
