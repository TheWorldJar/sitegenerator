import unittest
from blocks import *


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        # Test different heading levels
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEAD1)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEAD2)
        self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEAD3)
        self.assertEqual(block_to_block_type("#### Heading 4"), BlockType.HEAD4)
        self.assertEqual(block_to_block_type("##### Heading 5"), BlockType.HEAD5)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEAD6)

    def test_code(self):
        # Test code blocks
        self.assertEqual(block_to_block_type("```\ncode block\n```"), BlockType.CODE)
        self.assertEqual(
            block_to_block_type("```python\nprint('hello')\n```"), BlockType.CODE
        )
        self.assertEqual(
            block_to_block_type("```\nmulti\nline\ncode\n```"), BlockType.CODE
        )

    def test_quote(self):
        # Test quote blocks
        self.assertEqual(block_to_block_type("> Single line quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type("> First line\n> Second line"), BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type("> Quote with **bold** and _italic_"), BlockType.QUOTE
        )
        self.assertEqual(block_to_block_type(">Single line quote"), BlockType.QUOTE)
        self.assertEqual(
            block_to_block_type(">First line\n>Second line"), BlockType.QUOTE
        )
        self.assertEqual(
            block_to_block_type(">Quote with **bold** and _italic_"), BlockType.QUOTE
        )

    def test_unordered_list(self):
        # Test unordered list blocks
        self.assertEqual(block_to_block_type("- Single item"), BlockType.ULIST)
        self.assertEqual(
            block_to_block_type("- First item\n- Second item"), BlockType.ULIST
        )
        self.assertEqual(
            block_to_block_type("- Item with **bold** and _italic_"), BlockType.ULIST
        )

    def test_ordered_list(self):
        # Test ordered list blocks
        self.assertEqual(block_to_block_type("1. Single item"), BlockType.OLIST)
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item"), BlockType.OLIST
        )
        self.assertEqual(
            block_to_block_type("1. Item with **bold** and _italic_"), BlockType.OLIST
        )

    def test_paragraph(self):
        # Test paragraph blocks
        self.assertEqual(block_to_block_type("Regular paragraph text"), BlockType.PARA)
        self.assertEqual(
            block_to_block_type("Paragraph with **bold** and _italic_"), BlockType.PARA
        )
        self.assertEqual(block_to_block_type("Multi\nline\nparagraph"), BlockType.PARA)

    def test_edge_cases(self):
        # Test edge cases
        self.assertEqual(block_to_block_type(""), BlockType.PARA)  # Empty string
        self.assertEqual(block_to_block_type("   "), BlockType.PARA)  # Only whitespace
        self.assertEqual(block_to_block_type("\n\n\n"), BlockType.PARA)  # Only newlines
        self.assertEqual(
            block_to_block_type("#Heading without space"), BlockType.PARA
        )  # Invalid heading
        self.assertEqual(
            block_to_block_type("-Item without space"), BlockType.PARA
        )  # Invalid unordered list
        self.assertEqual(
            block_to_block_type("1.Item without space"), BlockType.PARA
        )  # Invalid ordered list

    def test_mixed_content(self):
        # Test mixed content that should be treated as paragraphs
        self.assertEqual(
            block_to_block_type("> First line\nSecond line"), BlockType.PARA
        )  # Mixed quote and regular text
        self.assertEqual(
            block_to_block_type("> First line\n- Second line"), BlockType.PARA
        )  # Mixed quote and list
        self.assertEqual(
            block_to_block_type("- First item\nSecond line"), BlockType.PARA
        )  # Mixed list and regular text
        self.assertEqual(
            block_to_block_type("1. First item\n- Second item"), BlockType.PARA
        )  # Mixed ordered and unordered list
        self.assertEqual(
            block_to_block_type("1. First item\n> Second line"), BlockType.PARA
        )  # Mixed list and quote
        self.assertEqual(
            block_to_block_type("> First line\n1. Second line"), BlockType.PARA
        )  # Mixed quote and list
        self.assertEqual(
            block_to_block_type("> First line\n- Second line\nThird line"),
            BlockType.PARA,
        )  # Mixed quote, list, and regular text
        self.assertEqual(
            block_to_block_type("1. First item\n2. Second item\nThird line"),
            BlockType.PARA,
        )  # Mixed ordered list and regular text
        self.assertEqual(
            block_to_block_type("- First item\n- Second item\nThird line"),
            BlockType.PARA,
        )  # Mixed unordered list and regular text


if __name__ == "__main__":
    unittest.main()
