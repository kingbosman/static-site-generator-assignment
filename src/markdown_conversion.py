from textnode import TextNode, TextType


# TODO: later at end of project support also for nested attributes
# so a bold can also be italic and vice versa etc
# do  this by finding the next instance of all delims instead
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
            recursive_nodes_demimiter_split(old_node.text, delimiter, text_type, [])
        )
    return newNodes


def recursive_nodes_demimiter_split(
    text: str,
    delimiter: str,
    text_type: TextType,
    current_list: list[TextNode] = [],
) -> list[TextNode]:
    split = text.split(delimiter, 2)
    if len(split) == 2:
        raise ValueError("Invalid markdown syntax")

    if len(split) <= 1:
        current_list.append(TextNode(split[0], TextType.TEXT))
        return current_list

    if split[0] == "":
        # bold first word
        current_list.append(TextNode(split[1], text_type))
        return recursive_nodes_demimiter_split(
            split[2], delimiter, text_type, current_list
        )

    current_list.extend(
        [
            TextNode(split[0], TextType.TEXT),
            TextNode(split[1], text_type),
        ]
    )

    if split[2] != "":
        return recursive_nodes_demimiter_split(
            split[2], delimiter, text_type, current_list
        )
    return current_list
