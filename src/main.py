from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitter import split_into_links

def main():
    node = TextNode(
            "This is text with a [link1](https://example.com/1) and [link2](https://example.com/2)",
            TextType.NORMAL
        )
    print(split_into_links([node]))

if __name__ == "__main__":
    main()
