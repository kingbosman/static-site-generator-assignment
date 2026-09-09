from enums import TextType
from textnode import TextNode


def main():
    node = TextNode("fancy title", TextType.BOLD)
    print(node)


main()
