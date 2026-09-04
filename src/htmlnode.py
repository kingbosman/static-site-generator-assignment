from typing import Optional


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[HTMLNode]] = None,
        props: Optional[dict[str, str]] = None,
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self) -> str:
        return f"tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props}"

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self) -> str:
        result = ""
        if not self.props:
            return result
        for i, v in self.props.items():
            result += f' {i}="{v}"'
        return result


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: Optional[dict[str, str]] = None
    ) -> None:
        super().__init__(tag, value, props=props)

    def __repr__(self) -> str:
        return f"tag:{self.tag}, value:{self.value}, props:{self.props}"

    def to_html(self) -> str:
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
