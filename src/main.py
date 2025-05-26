from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from splitter import markdown_to_blocks

def main():
    md = """
          This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items        
"""
    print(markdown_to_blocks(md))

if __name__ == "__main__":
    main()
