from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import *
from splitter import *
from conversion import markdown_to_html_node

def main():
    md = "1. This\n2. Is\n3. A bold\n4. Quote\n\nA **bold** choice of _words_!\n\n![image1](https://fake.adress.com/image1.png)"
    print(markdown_to_html_node(md).to_html())

if __name__ == "__main__":
    main()
