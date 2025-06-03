from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import *
from splitter import *
from conversion import markdown_to_html_node
from filemanip import *
import re
import os


def main():
    # md = "1. This\n2. Is\n3. A bold\n4. Quote\n\nA **bold** choice of _words_!\n\n![image1](https://fake.adress.com/image1.png)\n\n```\nThis is a code block\n```\n\n>This\n>Is\n>A\n>Proper\n>Quote"
    # print(markdown_to_html_node(md).to_html())
    copy_static_to_public()

    # md = "### This is a heading3 #4"
    # print(re.sub(r"^#{1,6}\s", "", md))


if __name__ == "__main__":
    main()
