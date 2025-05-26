from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitter import split_by_text

def main():
    node = TextNode(
            "This is **bold** text with more **bold** text",
            TextType.NORMAL
        )
    print(split_by_text([node], "**", TextType.BOLD))

if __name__ == "__main__":
    main()
