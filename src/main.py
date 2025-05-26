from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from blocks import *

def main():
    md = """1. This
2. Is
3. A
Quote"""
    print(md.split("\n"))
    print(block_to_block_type(md))

if __name__ == "__main__":
    main()
