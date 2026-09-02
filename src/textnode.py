from enum import Enum
from typing import Optional


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(
        self, text: str, text_type: TextType, url: Optional[str] = None
    ) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, node: object) -> bool:
        if not isinstance(node, TextNode):
            return False
        return self == node

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
