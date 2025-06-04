import unittest
from conversion import markdown_to_html_node
from htmlnode import ParentNode, LeafNode
from blocks import BlockType


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_empty_markdown(self):
        markdown = ""
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(result.children, [])

    def test_single_paragraph(self):
        markdown = "This is a paragraph"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].value, "This is a paragraph")

    def test_multiple_paragraphs(self):
        markdown = "First paragraph\n\nSecond paragraph"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 2)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].value, "First paragraph")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(result.children[1].children[0].value, "Second paragraph")

    def test_heading_levels(self):
        markdown = "# Heading 1\n\n## Heading 2\n\n### Heading 3"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[0].children[0].value, "Heading 1")
        self.assertEqual(result.children[1].tag, "h2")
        self.assertEqual(result.children[1].children[0].value, "Heading 2")
        self.assertEqual(result.children[2].tag, "h3")
        self.assertEqual(result.children[2].children[0].value, "Heading 3")

    def test_code_block(self):
        markdown = "```\ncode block\n```"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "pre")
        self.assertEqual(result.children[0].children[0].tag, "code")
        self.assertEqual(result.children[0].children[0].children[0].value, "code block")

    def test_quote_block(self):
        markdown = "> This is a quote"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "blockquote")
        self.assertEqual(result.children[0].children[0].value, "This is a quote")

    def test_unordered_list(self):
        markdown = "- Item 1\n- Item 2"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].tag, "ul")
        self.assertEqual(len(result.children[0].children[0].children), 2)
        self.assertEqual(result.children[0].children[0].children[0].tag, "li")
        self.assertEqual(
            result.children[0].children[0].children[0].children[0].value, "Item 1"
        )
        self.assertEqual(result.children[0].children[0].children[1].tag, "li")
        self.assertEqual(
            result.children[0].children[0].children[1].children[0].value, "Item 2"
        )

    def test_ordered_list(self):
        markdown = "1. Item 1\n2. Item 2"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 1)
        self.assertEqual(result.children[0].tag, "p")
        self.assertEqual(result.children[0].children[0].tag, "ol")
        self.assertEqual(len(result.children[0].children[0].children), 2)
        self.assertEqual(result.children[0].children[0].children[0].tag, "li")
        self.assertEqual(
            result.children[0].children[0].children[0].children[0].value, "Item 1"
        )
        self.assertEqual(result.children[0].children[0].children[1].tag, "li")
        self.assertEqual(
            result.children[0].children[0].children[1].children[0].value, "Item 2"
        )

    def test_mixed_content(self):
        markdown = "# Title\n\nThis is a paragraph with **bold** and _italic_ text\n\n- List item 1\n- List item 2"
        result = markdown_to_html_node(markdown)
        self.assertEqual(result.tag, "div")
        self.assertEqual(len(result.children), 3)
        self.assertEqual(result.children[0].tag, "h1")
        self.assertEqual(result.children[0].children[0].value, "Title")
        self.assertEqual(result.children[1].tag, "p")
        self.assertEqual(len(result.children[1].children), 5)
        self.assertEqual(
            result.children[1].children[0].value, "This is a paragraph with "
        )
        self.assertEqual(result.children[1].children[1].tag, "b")
        self.assertEqual(result.children[1].children[1].value, "bold")
        self.assertEqual(result.children[1].children[2].value, " and ")
        self.assertEqual(result.children[1].children[3].tag, "i")
        self.assertEqual(result.children[1].children[3].value, "italic")
        self.assertEqual(result.children[1].children[4].value, " text")
        self.assertEqual(result.children[2].tag, "p")
        self.assertEqual(result.children[2].children[0].tag, "ul")


if __name__ == "__main__":
    unittest.main()
