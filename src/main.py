from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print (dummy)

if __name__ == "__main__":
    main()
