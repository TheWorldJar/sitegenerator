import unittest

from splitter import split_into_nodes
from textnode import TextNode, TextType

class TestSplitter(unittest.TestCase):
    def test_normal_text(self):
        text = ["This is normal text"]
        result = split_into_nodes(text, "", TextType.NORMAL)
        expected = [TextNode("This is normal text", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_multiple_normal_texts(self):
        text = ["First text", "Second text", "Third text"]
        result = split_into_nodes(text, "", TextType.NORMAL)
        expected = [
            TextNode("First text", TextType.NORMAL),
            TextNode("Second text", TextType.NORMAL),
            TextNode("Third text", TextType.NORMAL)
        ]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = ["This is **bold** text"]
        result = split_into_nodes(text, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = ["This is _italic_ text"]
        result = split_into_nodes(text, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.ITALIC),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.ITALIC)
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = ["This is `code` text"]
        result = split_into_nodes(text, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.CODE),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.CODE)
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_segments(self):
        text = ["This is **bold** and this is also **bold**"]
        result = split_into_nodes(text, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is also ", TextType.BOLD),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.BOLD)
        ]
        self.assertEqual(result, expected)

    def test_invalid_bold_delimiter(self):
        text = ["This is **bold** text"]
        with self.assertRaises(Exception) as context:
            split_into_nodes(text, "_", TextType.BOLD)
        self.assertEqual(str(context.exception), "Invalid delimiter: _ for text type: TextType.BOLD")

    def test_invalid_italic_delimiter(self):
        text = ["This is _italic_ text"]
        with self.assertRaises(Exception) as context:
            split_into_nodes(text, "**", TextType.ITALIC)
        self.assertEqual(str(context.exception), "Invalid delimiter: ** for text type: TextType.ITALIC")

    def test_invalid_code_delimiter(self):
        text = ["This is `code` text"]
        with self.assertRaises(Exception) as context:
            split_into_nodes(text, "**", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid delimiter: ** for text type: TextType.CODE")

    def test_empty_text_list(self):
        text = []
        result = split_into_nodes(text, "", TextType.NORMAL)
        self.assertEqual(result, [])

    def test_empty_text_chunk(self):
        text = [""]
        result = split_into_nodes(text, "", TextType.NORMAL)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
    