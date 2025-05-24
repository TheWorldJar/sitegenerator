from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode

def main():
    dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print (dummy)
    dummy_html = dummy.to_html_node()
    print (dummy_html)

if __name__ == "__main__":
    main()
