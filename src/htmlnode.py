class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list = None, props: dict = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __eq__(self, other: "HTMLNode"):
        if self.tag == other.tag:
            if self.value == other.value:
                if self.children == other.children:
                    if self.props == other.props:
                        return True
        return False

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def to_html(self):
        raise NotImplementedError("to_html is not implemented")
    
    def props_to_html(self):
        result = ""
        if self.props != None:
            for key, value in self.props.items():
                result += f" {key}=\"{value}\""
        return result
    
class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        super().__init__(tag, value, [], props)

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag == "img":
            return f"<img {self.props_to_html()}>"
        elif self.value is None or self.value == "":
            raise ValueError("value cannot be empty")
        elif self.tag is None or self.tag == "":
            return f"{self.value}"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: dict = None):
        super().__init__(tag, None, children, props)

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("tag cannot be empty")
        elif self.children is None or len(self.children) == 0:
            raise ValueError("children cannot be empty")
        else:
            return f"<{self.tag}{self.props_to_html()}>" + "".join(map(lambda x: x.to_html(), self.children)) + f"</{self.tag}>"