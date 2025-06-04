import unittest

from splitter import *
from textnode import TextNode, TextType


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        text = ["This is an image ![alt text](https://example.com/image.png)"]
        result = extract_markdown_images(text)
        expected = [("alt text", "https://example.com/image.png")]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text = [
            "First image ![alt1](https://example.com/image1.png)",
            "Second image ![alt2](https://example.com/image2.png)",
        ]
        result = extract_markdown_images(text)
        expected = [
            ("alt1", "https://example.com/image1.png"),
            ("alt2", "https://example.com/image2.png"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images_in_single_line(self):
        text = [
            "![alt1](https://example.com/image1.png) and ![alt2](https://example.com/image2.png)"
        ]
        result = extract_markdown_images(text)
        expected = [
            ("alt1", "https://example.com/image1.png"),
            ("alt2", "https://example.com/image2.png"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text = ["This is a text without any images"]
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_empty_text(self):
        text = [""]
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_empty_list(self):
        text = []
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_invalid_image_syntax(self):
        text = ["This is not an image [alt](https://example.com/image.png)"]
        result = extract_markdown_images(text)
        self.assertEqual(result, [])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        text = ["This is a link [link text](https://example.com)"]
        result = extract_markdown_links(text)
        expected = [("link text", "https://example.com")]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text = [
            "First link [link1](https://example.com/1)",
            "Second link [link2](https://example.com/2)",
        ]
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links_in_single_line(self):
        text = ["[link1](https://example.com/1) and [link2](https://example.com/2)"]
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text = ["This is a text without any links"]
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_empty_text(self):
        text = [""]
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_empty_list(self):
        text = []
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_links_with_special_chars(self):
        text = ["[link!@#$%](https://example.com/path!@#$%)"]
        result = extract_markdown_links(text)
        expected = [("link!@#$%", "https://example.com/path!@#$%")]
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text = [
            "Here's a link [link1](https://example.com/1)",
            "And an image ![alt](https://example.com/image.png)",
            "And another link [link2](https://example.com/2)",
        ]
        result = extract_markdown_links(text)
        expected = [
            ("link1", "https://example.com/1"),
            ("link2", "https://example.com/2"),
        ]
        self.assertEqual(result, expected)
        result = extract_markdown_images(text)
        expected = [("alt", "https://example.com/image.png")]
        self.assertEqual(result, expected)


class TestSplitIntoImages(unittest.TestCase):
    def test_single_image(self):
        text_nodes = [
            TextNode(
                "This is an image ![alt text](https://example.com/image.png)",
                TextType.NORMAL,
            )
        ]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("This is an image ", TextType.NORMAL),
            TextNode("alt text", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_images(self):
        text_nodes = [
            TextNode(
                "![alt1](https://example.com/image1.png) and ![alt2](https://example.com/image2.png)",
                TextType.NORMAL,
            )
        ]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("alt1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("alt2", TextType.IMAGE, "https://example.com/image2.png"),
        ]
        self.assertEqual(result, expected)

    def test_no_images(self):
        text_nodes = [TextNode("This is text without any images", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [TextNode("This is text without any images", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text_nodes = [TextNode("", TextType.NORMAL)]
        result = split_into_images(text_nodes)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        text_nodes = []
        result = split_into_images(text_nodes)
        self.assertEqual(result, [])

    def test_multiple_nodes(self):
        text_nodes = [
            TextNode(
                "First node ![alt1](https://example.com/image1.png)", TextType.NORMAL
            ),
            TextNode(
                "Second node ![alt2](https://example.com/image2.png)", TextType.NORMAL
            ),
        ]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("First node ", TextType.NORMAL),
            TextNode("alt1", TextType.IMAGE, "https://example.com/image1.png"),
            TextNode("Second node ", TextType.NORMAL),
            TextNode("alt2", TextType.IMAGE, "https://example.com/image2.png"),
        ]
        self.assertEqual(result, expected)

    def test_image_at_start(self):
        text_nodes = [
            TextNode(
                "![alt](https://example.com/image.png) This is text after the image",
                TextType.NORMAL,
            )
        ]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("alt", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" This is text after the image", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_image_at_end(self):
        text_nodes = [
            TextNode(
                "This is text before the image ![alt](https://example.com/image.png)",
                TextType.NORMAL,
            )
        ]
        result = split_into_images(text_nodes)
        expected = [
            TextNode("This is text before the image ", TextType.NORMAL),
            TextNode("alt", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(result, expected)


class TestSplitIntoLinks(unittest.TestCase):
    def test_single_link(self):
        text_nodes = [
            TextNode("This is a link [link text](https://example.com)", TextType.NORMAL)
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("This is a link ", TextType.NORMAL),
            TextNode("link text", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_multiple_links(self):
        text_nodes = [
            TextNode(
                "[link1](https://example.com/1) and [link2](https://example.com/2)",
                TextType.NORMAL,
            )
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
        ]
        self.assertEqual(result, expected)

    def test_no_links(self):
        text_nodes = [TextNode("This is text without any links", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [TextNode("This is text without any links", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text_nodes = [TextNode("", TextType.NORMAL)]
        result = split_into_links(text_nodes)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        text_nodes = []
        result = split_into_links(text_nodes)
        self.assertEqual(result, [])

    def test_multiple_nodes(self):
        text_nodes = [
            TextNode("First node [link1](https://example.com/1)", TextType.NORMAL),
            TextNode("Second node [link2](https://example.com/2)", TextType.NORMAL),
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("First node ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode("Second node ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
        ]
        self.assertEqual(result, expected)

    def test_link_at_start(self):
        text_nodes = [
            TextNode(
                "[link](https://example.com) This is text after the link",
                TextType.NORMAL,
            )
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" This is text after the link", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_link_at_end(self):
        text_nodes = [
            TextNode(
                "This is text before the link [link](https://example.com)",
                TextType.NORMAL,
            )
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("This is text before the link ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(result, expected)

    def test_mixed_content(self):
        text_nodes = [
            TextNode("Here's a link [link1](https://example.com/1)", TextType.NORMAL),
            TextNode(
                "And an image ![alt](https://example.com/image.png)", TextType.NORMAL
            ),
            TextNode(
                "And another link [link2](https://example.com/2)", TextType.NORMAL
            ),
        ]
        result = split_into_links(text_nodes)
        expected = [
            TextNode("Here's a link ", TextType.NORMAL),
            TextNode("link1", TextType.LINK, "https://example.com/1"),
            TextNode(
                "And an image ![alt](https://example.com/image.png)", TextType.NORMAL
            ),
            TextNode("And another link ", TextType.NORMAL),
            TextNode("link2", TextType.LINK, "https://example.com/2"),
        ]
        self.assertEqual(result, expected)


class TestSplitByText(unittest.TestCase):
    def test_bold_text(self):
        text_nodes = [TextNode("This is **bold** text", TextType.NORMAL)]
        result = split_by_text(text_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text_nodes = [TextNode("This is _italic_ text", TextType.NORMAL)]
        result = split_by_text(text_nodes, "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text_nodes = [TextNode("This is `code` text", TextType.NORMAL)]
        result = split_by_text(text_nodes, "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_multiple_bold_segments(self):
        text_nodes = [
            TextNode("This is **bold** and this is also **bold**", TextType.NORMAL)
        ]
        result = split_by_text(text_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and this is also ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode("", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_multiple_nodes(self):
        text_nodes = [
            TextNode("First **bold** text", TextType.NORMAL),
            TextNode("Second **bold** text", TextType.NORMAL),
        ]
        result = split_by_text(text_nodes, "**", TextType.BOLD)
        expected = [
            TextNode("First ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
            TextNode("Second ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_no_delimiters(self):
        text_nodes = [TextNode("This is normal text", TextType.NORMAL)]
        result = split_by_text(text_nodes, "**", TextType.BOLD)
        expected = [TextNode("This is normal text", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text_nodes = [TextNode("", TextType.NORMAL)]
        result = split_by_text(text_nodes, "**", TextType.BOLD)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        text_nodes = []
        result = split_by_text(text_nodes, "**", TextType.BOLD)
        self.assertEqual(result, [])

    def test_invalid_delimiter(self):
        text_nodes = [TextNode("This is **bold** text", TextType.NORMAL)]
        with self.assertRaises(Exception) as context:
            split_by_text(text_nodes, "_", TextType.BOLD)
        self.assertEqual(
            str(context.exception), "Invalid delimiter: _ for text type: TextType.BOLD"
        )


class TestTextToNodes(unittest.TestCase):
    def test_plain_text(self):
        text = "This is plain text"
        result = text_to_nodes(text)
        expected = [TextNode("This is plain text", TextType.NORMAL)]
        self.assertEqual(result, expected)

    def test_bold_text(self):
        text = "This is **bold** text"
        result = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_italic_text(self):
        text = "This is _italic_ text"
        result = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_code_text(self):
        text = "This is `code` text"
        result = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_link_text(self):
        text = "This is a [link](https://example.com) text"
        result = text_to_nodes(text)
        expected = [
            TextNode("This is a ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_image_text(self):
        text = "This is an ![image](https://example.com/image.png) text"
        result = text_to_nodes(text)
        expected = [
            TextNode("This is an ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" text", TextType.NORMAL),
        ]
        self.assertEqual(result, expected)

    def test_mixed_text(self):
        text = "This is **bold** and _italic_ with `code` and [link](https://example.com) and ![image](https://example.com/image.png)"
        result = text_to_nodes(text)
        expected = [
            TextNode("This is ", TextType.NORMAL),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.NORMAL),
            TextNode("italic", TextType.ITALIC),
            TextNode(" with ", TextType.NORMAL),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.NORMAL),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text = ""
        result = text_to_nodes(text)
        expected = [TextNode("", TextType.NORMAL)]
        self.assertEqual(result, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_block(self):
        text = "This is a single block"
        result = markdown_to_blocks(text)
        expected = ["This is a single block"]
        self.assertEqual(result, expected)

    def test_multiple_blocks(self):
        text = """This is the first block

This is the second block

This is the third block"""
        result = markdown_to_blocks(text)
        expected = [
            "This is the first block",
            "This is the second block",
            "This is the third block",
        ]
        self.assertEqual(result, expected)

    def test_blocks_with_extra_newlines(self):
        text = """This is the first block


This is the second block


This is the third block"""
        result = markdown_to_blocks(text)
        expected = [
            "This is the first block",
            "This is the second block",
            "This is the third block",
        ]
        self.assertEqual(result, expected)

    def test_blocks_with_leading_trailing_spaces(self):
        text = """   This is the first block   

   This is the second block   

   This is the third block   """
        result = markdown_to_blocks(text)
        expected = [
            "This is the first block",
            "This is the second block",
            "This is the third block",
        ]
        self.assertEqual(result, expected)

    def test_blocks_with_mixed_content(self):
        text = """# This is a heading

This is a paragraph with **bold** and _italic_ text

- This is a list item
- This is another list item

> This is a blockquote"""
        result = markdown_to_blocks(text)
        expected = [
            "# This is a heading",
            "This is a paragraph with **bold** and _italic_ text",
            "- This is a list item\n- This is another list item",
            "> This is a blockquote",
        ]
        self.assertEqual(result, expected)

    def test_empty_text(self):
        text = ""
        result = markdown_to_blocks(text)
        expected = []
        self.assertEqual(result, expected)

    def test_text_with_only_newlines(self):
        text = "\n\n\n"
        result = markdown_to_blocks(text)
        expected = []
        self.assertEqual(result, expected)

    def test_text_with_only_spaces(self):
        text = "   \n   \n   "
        result = markdown_to_blocks(text)
        expected = []
        self.assertEqual(result, expected)


class TestExtractTitle(unittest.TestCase):
    def test_valid_title_and_body(self):
        text = "# My Title\n\nThis is the body text"
        result = extract_title(text)
        expected = ("My Title", "This is the body text")
        self.assertEqual(result, expected)

    def test_no_title(self):
        text = "This is not a title\n\nThis is the body text"
        with self.assertRaises(Exception) as context:
            extract_title(text)
        self.assertEqual(str(context.exception), "Document title not found on the fist line!")

    def test_title_without_body(self):
        text = "# My Title"
        result = extract_title(text)
        expected = ("My Title", "")
        self.assertEqual(result, expected)

    def test_title_with_empty_body(self):
        text = "# My Title\n\n"
        result = extract_title(text)
        expected = ("My Title", "")
        self.assertEqual(result, expected)

    def test_title_with_special_chars(self):
        text = "# My Title with !@#$%^&*()\n\nThis is the body"
        result = extract_title(text)
        expected = ("My Title with !@#$%^&*()", "This is the body")
        self.assertEqual(result, expected)

    def test_title_with_extra_spaces(self):
        text = "#   My Title with extra spaces   \n\nThis is the body"
        result = extract_title(text)
        expected = ("My Title with extra spaces", "This is the body")
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
